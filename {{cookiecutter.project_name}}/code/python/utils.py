import pandas as pd
from pandas_profiling import ProfileReport
from bs4 import BeautifulSoup
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

test_data = pd.read_parquet(
    "/home/ulgu3559/oda-repos/yield-model/data/transformed/yield.parquet"
).filter(
    items=[
        "YEAR",
        "RESIDENCY_STATUS",
        "ETHNICITY",
        "ADDRESS_REGION",
        "PERSON_FAMILY_SIZE",
        "PERSON_HS_RANK_PERCENTILE",
        "DEPOSIT_PAID",
    ]
)

template = Environment(
    loader=FileSystemLoader(Path("../../code/python/templates").resolve())
).get_template("report.html")


def eda_report_by_partition(df: pd.DataFrame, col_name: str):
    if col_name in df.columns:
        overview_section = {}
        variables_section = {}
        for group in df.groupby(col_name):
            partition_name = group[0]
            _ = pd.DataFrame(group[1]).reset_index()
            dom = BeautifulSoup(
                ProfileReport(_, minimal=True).to_html(), features="html.parser"
            )
            overview_section.setdefault(partition_name, []).extend(
                dom.select("#overview-dataset_overview")
            )
            overview_section.setdefault(partition_name, []).extend(
                dom.select("#overview-warnings")
            )
            features = dom.select(".variable")
            for feature in features:
                # relies on the pandas profiling report structure
                feature_name = feature.div.p["title"]
                variables_section.setdefault(partition_name, {}).setdefault(
                    feature_name, []
                ).extend(feature)
        with open("hello.html", "w") as fh:
            fh.write(
                template.render(
                    overview_section=overview_section,
                    variables_section=variables_section,
                )
            )


eda_report_by_partition(test_data, "YEAR")

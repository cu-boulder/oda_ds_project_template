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


def eda_report_by_partition(df: pd.DataFrame, partition: str) -> pd.DataFrame:
    if partition in df.columns:
        partitions = df.groupby(partition)
        variables_section = []
        for group in partitions:
            partition_name = group[0]
            _ = pd.DataFrame(group[1]).reset_index()
            section_items = BeautifulSoup(
                ProfileReport(_, minimal=True).to_html(), features="html.parser"
            ).find_all("div", attrs={"class": "section-items"})
            variables_section.extend(section_items)
        with open("hello.html", "w") as fh:
            fh.write(template.render(variables_section=variables_section))


eda_report_by_partition(test_data, "YEAR")

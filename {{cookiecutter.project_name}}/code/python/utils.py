import pandas as pd
from pandas_profiling import ProfileReport
from bs4 import BeautifulSoup
from typing import Union
from pathlib import Path
from jinja2 import Environment, FileSystemLoader



def get_report_template(template: str):
    return Environment(
        loader=FileSystemLoader(Path("../../code/python/templates").resolve())
    ).get_template(template)


def eda_report_by_partition(
    df: pd.DataFrame, partition: str, report_name: str = "eda_report_by_partition"
):
    if partition in df.columns:
        overview_section = {}
        features_section = {}
        for group in df.groupby(partition):
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
            for feature in dom.select(".variable"):
                feature_name = feature.div.p["title"]
                features_section.setdefault(feature_name, {}).setdefault(
                    partition_name, []
                ).append(feature)
        # relies on the current project folder structure
        out_path = Path("../../outputs/reports").resolve()
        template = get_report_template("eda_by_partition.html")
        with open(out_path / f"{report_name}.html", "w") as report:
            report.write(
                template.render(
                    overview_section=overview_section,
                    features_section=features_section,
                )
            )
    else:
        raise KeyError(f"{partition} is missing from columns")
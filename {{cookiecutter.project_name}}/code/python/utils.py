import pandas as pd
from pandas_profiling import ProfileReport
from bs4 import BeautifulSoup
from typing import Union
from pathlib import Path
from jinja2 import Environment, FileSystemLoader



def get_report_template(template: str):
    """Gets a Jinja2 html template from the templates folder.

    Args:
        template (str): Jinja2 html template

    """
    return Environment(
        loader=FileSystemLoader(Path("../../code/python/templates").resolve())
    ).get_template(template)


def eda_report_by_partition(
    df: pd.DataFrame, partition: str, report_name: str = "eda_report_by_partition"
):
    """Generate a profile report by partition from a pandas DataFrame.

    Args:
        df (pd.DataFrame)
        partition (str): An existing column in the DataFrame which values should
        be used as partitions.
        report_name (str, optional): The name of the html report. 
        Defaults to "eda_report_by_partition".

    Raises:
        KeyError: The partition name is not in the provided DataFrame
    """
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
import logging
from functools import wraps
from pathlib import Path
from typing import Callable, Union

import great_expectations as ge
import pandas as pd
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from pandas_profiling import ProfileReport

logger = logging.getLogger(__name__)


def get_report_template(template: str):
    """Get a Jinja2 html template from the templates folder.

    Args:
        template (str): Jinja2 html template

    """
    return Environment(
        loader=FileSystemLoader(Path(__file__).resolve().parents[0] / "templates")
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
        out_path = Path(__file__).resolve().parents[2] / "outputs/reports"
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


def validate_expectations(
    suite_name: str,
    expectations_dir: Path = Path(__file__).parents[1].resolve()
    / "great_expectations/expectations",
) -> Callable:
    """Validate a Pandas DataFrame using a Great Expectations suite.
    Args:
        suite_name (str): A valid json Great Expectations suite
        expectations_dir (Path, optional): Great Expectations folder location.
        Defaults to Path(__file__).parents[1].resolve()/"great_expectations/expectations".
    Returns:
        Callable
    """

    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            df = function()
            if not isinstance(df, pd.DataFrame):
                raise ValueError(
                    "The decorated function must return a Pandas DataFrame"
                )
            if suite_name is None:
                raise ValueError("A suite name is required")
            if not suite_name.endswith(".json"):
                raise ValueError(
                    "The suite name should be a valid json expectation suite"
                )
            suite_path = expectations_dir / suite_name
            if not suite_path.exists():
                raise FileNotFoundError("The suite could not be found")
            validation_result = ge.from_pandas(df).validate(
                expectation_suite=str(suite_path)
            )
            if not validation_result["success"]:
                for result in validation_result["results"]:
                    if not result["success"]:
                        logger.error(msg=result["expectation_config"])
                raise GreatExpectationsError("The dataframe did not meet expectations")
            return df

        return wrapper

    return decorator

import pandas as pd
from pandas_profiling import ProfileReport
from bs4 import BeautifulSoup
from jinja2 import Template

test_data = pd.read_parquet(
    "/home/ulgu3559/oda-repos/yield-model/data/transformed/yield.parquet"
)



def eda_report_by_partition(df: pd.DataFrame, partition: str) -> pd.DataFrame:
    if partition in df.columns:
        partitions = df.groupby(partition)
        for group in partitions:
            partition_name = group[0]
            _ = pd.DataFrame(group[1])
            soup = BeautifulSoup(ProfileReport(_, minimal=True).to_html()).find_all(
                "div", attrs={"class": "section-items"}
            )
            print(soup)


eda_report_by_partition(test_data, "YEAR")

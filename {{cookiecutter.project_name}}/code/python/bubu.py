import pandas as pd
from utils import eda_report_by_partition


test_data = pd.read_parquet(
    "/home/ulgu3559/oda-repos/yield-model/data/transformed/yield.parquet"
)

eda_report_by_partition(test_data, "YEAR")
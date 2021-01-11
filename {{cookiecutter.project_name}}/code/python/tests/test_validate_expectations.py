import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

# Ensures that the code in src can be run and accessed from the console:
# see importing sibling packages in Python
sys.path.append(str(Path(__file__).parents[1].resolve()))

from utils import validate_expectations


def test_validate_expectations_non_df():
    with pytest.raises(ValueError, match="must return a Pandas DataFrame$"):

        @validate_expectations(suite_name="person_status.json")
        def non_df():
            x = pd.DataFrame(
                columns=[
                    "person_id",
                    "person_name",
                    "person_created",
                    "person_status",
                    "status_timestamp",
                ]
            ).to_numpy()

        non_df()


def test_validate_expectations_suite_non_valid_suite_name():
    with pytest.raises(ValueError, match="valid json expectation suite$"):

        @validate_expectations(suite_name="")
        def df():
            return pd.DataFrame(
                {
                    "person_id": pd.Series(
                        ["17829292", "1782955657", "17829292"], dtype="string"
                    ),
                    "person_status": pd.Series(
                        ["Applicant", "Inquiry", "Prospect"], dtype="string"
                    ),
                }
            )

        df()

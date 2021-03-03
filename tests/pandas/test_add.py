from pandas.testing import assert_series_equal
import pandas as pd
from src.pandas.add import AddTwoColumns


class TestAddTwoColumns:
    def test_add_two_columns(self):
        df = pd.DataFrame(
            {
                "column_1": [23.0, pd.NA, 23.0, -23.0],
                "column_2": [12.0, 12.0, pd.NA, -12.0],
            }
        )
        result = AddTwoColumns.calculate(self, df, "column_1", "column_2")
        expected_result = pd.Series([35.0, pd.NA, pd.NA, -35.0], index=df.index)

        assert_series_equal(result, expected_result)

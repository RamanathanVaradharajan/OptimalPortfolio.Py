"""
Test inputs.
"""
from pandas.testing import assert_frame_equal
import pandas as pd
from src.stock_calculator.inputs import Inputs


class TestInputs:
    """
    This class contains test functions for inputs.

    Functions tested:
    Inputs.read_inputs(filepath: str)
    """

    def test_read_inputs(self):
        """
        Test the read_inputs() function.

        Test excel file is located in the tests/dataframes/input/ folder.
        """
        result_df = Inputs().read_inputs(
            r"./tests/dataframes/input/input_portfolio.xlsx"
        )
        expected_df = pd.DataFrame(
            {
                "Stock_ID": [4, 5, 3, 2, 6, 1],
                "Stock": ["RDS-A", "PLTR", "TSLA", "AMZN", "ENPH", "GOOG"],
                "Amount": [25314.52, 5274.84, 4300.02, 3352.27, 777.44, 223.11],
            }
        ).set_index("Stock_ID")
        assert_frame_equal(result_df, expected_df)

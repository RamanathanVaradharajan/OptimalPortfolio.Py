"""
Test inputs.
"""
import pandas as pd
from pandas.testing import assert_frame_equal

from src.ultron.stock_inputs import StockInputs


class TestStockInputs:
    """
    This class contains test functions for stock inputs.

    Functions tested:
    StockInputs.read()
    """

    def test_read(self):
        """
        Test the read() function.

        Test excel file is located in the src/dataframes/input/input_portfolio.xlsx.
        """
        result_df = StockInputs().read()
        expected_df = pd.DataFrame(
            {
                "Stock_ID": list(range(1, 11)),
                "Stock": [
                    "GOOG",
                    "MSFT",
                    "FB",
                    "AAPL",
                    "ARKF",
                    "ENPH",
                    "AMZN",
                    "TSLA",
                    "PLTR",
                    "RDS-A",
                ],
                "Amount": [
                    606.93,
                    567.70,
                    617.34,
                    214.80,
                    418.56,
                    891.98,
                    3451.95,
                    4986.22,
                    5934.47,
                    25626.40,
                ],
            }
        ).set_index("Stock_ID")
        assert_frame_equal(result_df, expected_df, check_exact=True)

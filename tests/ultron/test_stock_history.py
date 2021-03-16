import pandas as pd
import yfinance as yf
from pandas.testing import assert_frame_equal, assert_series_equal

from src.ultron.stock_history import StockHistory


class TestStockHistory:
    """
    This class contains test functions for stock history.

    Functions tested:
    StockHistory(period, interval, stocks).get()
    """

    def test_get_with_valid_tickers(self):
        result_df = StockHistory(
            period="5d", interval="1d", stocks=["GOOG", "PLTR"]
        ).get()
        expected_df = (yf.download(["GOOG", "PLTR"], period="5d", interval="1d"))[
            "Close"
        ]

        assert_frame_equal(result_df, expected_df, check_exact=True)

    def test_get_with_wrong_tickers(self):
        result_df = StockHistory(period="5d", interval="1d", stocks=["GILLL"]).get()
        expected_df = (yf.download(["Delisted"], period="5d", interval="1d"))["Close"]
        assert_series_equal(result_df, expected_df, check_exact=True)

    def test_get_with_one_valid_tickers(self):
        result_df = StockHistory(
            period="5d", interval="1d", stocks=["GOOG", "Delisted"]
        ).get()
        expected_df = (yf.download(["GOOG", "Delisted"], period="5d", interval="1d"))[
            "Close"
        ]

        assert_frame_equal(result_df, expected_df, check_exact=True)

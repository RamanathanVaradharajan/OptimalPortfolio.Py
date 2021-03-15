import pandas as pd
import yfinance as yf


class StockHistory:
    """
    Get the stock close price.
    :parameters
            period: str = Period over which the history will be collected.
            stocks: [list] = List of stock ticker signs from the input stock_df.
            interval: str = Interval over which the history should be collected.
    """

    def __init__(self, period: str, interval: str, stocks: list):
        self.period = period
        self.interval = interval
        self.stocks = stocks

    def get(self) -> pd.DataFrame:
        """
        Get the stock history.
        :return Pandas Dataframe containing the close price.
        """
        return yf.download(
            self.stocks,
            period=self.period,
            interval=self.interval,
            progress=False,
        )

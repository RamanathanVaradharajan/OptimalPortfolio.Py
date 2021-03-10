import pandas as pd
import yfinance as yf


class YahooFinance:
    """
    Get the closing price of a stock ticker.
    Use the yfinance library.
    """

    def all_history(self, stocks: list):
        daily_history = self.get_history(stocks, "1d")
        monthly_history = self.get_history(stocks, "1mo")
        quarterly_history = self.get_history(stocks, "3mo")
        return daily_history, monthly_history, quarterly_history

    def get_history(self, stock_list: list, intervals: str) -> pd.DataFrame:
        """Get the stock close price.
        :parameters
            stock_list: [list] = List of stock ticker signs.
            interval: str = Interval over which the history is collected.
        """

        return yf.download(
            stock_list,
            period="1wk",
            progress=False,
            interval=intervals,
        )

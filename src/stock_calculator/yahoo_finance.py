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


"""
    def get_close_price(
        self, stock_list: list, period: str, interval: str
    ) -> pd.Series:
        Get the stock close price.
        :parameters
            stock_list: [list] = List of stock ticker signs.
            period: str = Period over which the stock price is returned.
            interval: str = Use to specify the interval.
        

        df = yf.download(
            stock_list,
            period=period,
            progress=False,
            interval=interval,
        )
        print(df.head())
        return df["Close"]

if __name__ == "__main__":
    input_df = pd.read_excel(
        r"./../dataframes/input/input_portfolio.xlsx", index_col="Stock_ID"
    )
    print(input_df)

    stock_list = list(input_df["Stock"])
    close_price = YahooFinance().get_close_price(
        stock_list, period="1y", interval="1mo"
    )
    print(close_price)
    # print((close_price.pct_change().std()).reset_index(drop=True))
    avg_return = close_price.pct_change().std()
    # avg_return.index = input_df.index

    new_df = pd.DataFrame(
        {"Stock": avg_return.index.values, "Return": avg_return.values}
    )
    print(new_df)
    merged_df = (input_df.merge(new_df, on="Stock", how="left")).set_index(
        input_df.index
    )
    print(merged_df)
    # new_df = (input_df.reset_index()).set_index(["Stock"])
    # print(new_df.merge(avg_return, left_index=True, right_index=True))
    # print(input_df)

    # input_df["Return"] = avg_return
    # print(input_df)
"""
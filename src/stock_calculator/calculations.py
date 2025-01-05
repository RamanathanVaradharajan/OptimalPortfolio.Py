import numpy as np
import pandas as pd
import yfinance as yf
from src.attributes import excel_input_names as inp


class Calculate:
    count = 0

    def returns(self, history_df: pd.DataFrame, input_df: pd.DataFrame, stock_list: list):
        """Determine the average returns.
        :parameters
            history_df: DataFrame -> dataframe containing the historical
             close prices.
            input_df: DataFrame -> dataframe containing the details about
             stocks in portfolio.
        """

        averaged_returns = history_df["Close"].pct_change().mean()

        # corrections for dividends 
        # turn on if yfinance<0.2.51
        for stock in stock_list:
            dividends = pd.DataFrame(yf.Ticker(stock).dividends).reset_index()
            dividends["Date"] = pd.to_datetime(dividends["Date"].dt.strftime("%Y-%m-%d %H:%M:%S"))
            dividends.set_index("Date", inplace=True)
            frame = pd.concat([history_df["Close"][stock],dividends["Dividends"]],axis=1)
            # frame["Close"] = frame[stock]+frame["Dividends"].fillna(0)
            # frame["Return"] = (frame["Close"]-frame[stock].shift(1))/frame[stock].shift(1)
            # averaged_returns[stock]=frame["Return"].mean()

        

        temp_df = pd.DataFrame(
            {
                "Stock": averaged_returns.index.values,
                "Return": averaged_returns.values,
            },
        )

        merged_df = (input_df.merge(temp_df, on="Stock", how="left")).set_index(
            input_df.index
        )

        return ((1+merged_df["Return"])**252)-1

    def volatility(self, history_df: pd.DataFrame, input_df: pd.DataFrame):
        """Determine the standard deviation.
        :parameters
            history_df: DataFrame -> dataframe containing the historical
             close prices.
            input_df: DataFrame -> dataframe containing the details about
             stocks in portfolio.
        """
        averaged_volatility = history_df["Close"].pct_change().std()

        temp_df = pd.DataFrame(
            {
                "Stock": averaged_volatility.index.values,
                "Volatility": averaged_volatility.values,
            }
        )

        merged_df = (input_df.merge(temp_df, on="Stock", how="left")).set_index(
            input_df.index
        )

        return merged_df["Volatility"]*(252**0.5)

    def portfolio_volatility(
        self,
        weights: np.ndarray,
        history_df: pd.DataFrame,
        input_df: pd.DataFrame,
        covi: np.ndarray
    ):
        weight = weights
        # self.count += 1
        # TODO: Do not have to calculate the covariance matrix during
        #  every iteration.
        # if self.count % 10 == 0:
        #     print(f"Iterating step: {self.count}. Weight: {np.around(weight, 2)}")
        # stocks = list(input_df["Stock"])
        # covariance_matrix = np.zeros((len(stocks), len(stocks)))
        # for id1, stock1 in enumerate(stocks):
        #     for id2, stock2 in enumerate(stocks):
        #         covariance_matrix[id1][id2] = (
        #             history_df["Close"][stock1]
        #             .pct_change()
        #             .cov(history_df["Close"][stock2].pct_change())
        #         )

        # TODO: separate it into methods.
        # Use covariance matrix as separate method.
        # Use a method to get portfolio return and standard deviation.
        # Use a method to get sharpe ratio
        # (portfolio return - market return)/portfolio standard deviation
        # TODO: Covariance df should be output of covariance method.
        # covariance_df = pd.DataFrame(
        # covariance_matrix, columns=stocks, index=stocks)
        portfolio_return = weight.dot(input_df["Daily_Return"])
        portfolio_std = np.sqrt(np.dot(weight.T, np.dot(weight.T, covi)))*np.sqrt(252)
        # multiply by sqrt(252) to get annualized sharp ratio
        return - ((portfolio_return - inp.risk_free_rate)/ portfolio_std)

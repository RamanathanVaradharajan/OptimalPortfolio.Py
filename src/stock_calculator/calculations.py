import numpy as np
import pandas as pd


class Calculate:
    def returns(self, history_df: pd.DataFrame, input_df: pd.DataFrame):
        """Determine the average returns.
        :parameters
            history_df: DataFrame -> dataframe containing the historical
             close prices.
            input_df: DataFrame -> dataframe containing the details about
             stocks in portfolio.
        """

        averaged_returns = history_df["Close"].pct_change().mean()

        temp_df = pd.DataFrame(
            {
                "Stock": averaged_returns.index.values,
                "Return": averaged_returns.values,
            },
        )

        merged_df = (
            input_df.merge(temp_df, on="Stock", how="left")
        ).set_index(input_df.index)

        return merged_df["Return"]

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

        merged_df = (
            input_df.merge(temp_df, on="Stock", how="left")
        ).set_index(input_df.index)

        return merged_df["Volatility"]

    def portfolio_volatility(
        self,
        weights: np.array,
        history_df: pd.DataFrame,
        input_df: pd.DataFrame,
    ):
        weight = weights
        # TODO: Do not have to calculate the covariance matrix during
        #  every iteration.
        stocks = list(input_df["Stock"])
        covariance_matrix = np.zeros((len(stocks), len(stocks)))
        for id1, stock1 in enumerate(stocks):
            for id2, stock2 in enumerate(stocks):
                covariance_matrix[id1][id2] = (
                    history_df["Close"][stock1]
                    .pct_change()
                    .cov(history_df["Close"][stock2].pct_change())
                )

        # TODO: separate it into methods.
        # Use covariance matrix as separate method.
        # Use a method to get portfolio return and standard deviation.
        # Use a method to get sharpe ratio
        # (portfolio return - market return)/portfolio standard deviation
        # TODO: Covariance df should be output of covariance method.
        # covariance_df = pd.DataFrame(
        # covariance_matrix, columns=stocks, index=stocks)
        portfolio_return = weight.dot(input_df["Daily_Return"])
        portfolio_std = np.sqrt((weight.dot(covariance_matrix)).dot(weight))
        return 1.0 - (portfolio_return / portfolio_std)

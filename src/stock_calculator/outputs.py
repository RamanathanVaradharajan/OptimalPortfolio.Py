import numpy as np
import pandas as pd
from scipy.optimize import minimize

from src.stock_calculator.calculations import Calculate


class Output:
    def put_outputs(
        self,
        df: pd.DataFrame,
        daily_history: pd.DataFrame,
        monthly_history: pd.DataFrame,
        quarterly_history: pd.DataFrame,
    ):
        df["Daily_Return"] = Calculate().returns(daily_history, df)
        # df["Monthly_Return"] = Calculate().returns(monthly_history, df)
        # df["Quarterly_Return"] = Calculate().returns(quarterly_history, df)
        df["Volatility"] = Calculate().volatility(daily_history, df)
        weights = (df["Amount"] / df["Amount"].sum()).to_numpy()
        df["Original_Allocation"] = weights

        stocks = df["Stock"]
        covariance_matrix = np.zeros((len(stocks), len(stocks)))
        for id1, stock1 in enumerate(stocks):
            for id2, stock2 in enumerate(stocks):
                covariance_matrix[id1][id2] = (
                    daily_history["Close"][stock1]
                    .pct_change()
                    .cov(daily_history["Close"][stock2].pct_change())
                )

        neg_sharpe_ratio = Calculate().portfolio_volatility(weights, daily_history, df, covariance_matrix)
        expected_return = (df["Original_Allocation"] * df["Daily_Return"]).sum()
        expected_std = (expected_return-0.0425) / (-1*neg_sharpe_ratio)
        print("Sharpe ratio: ", -1*neg_sharpe_ratio)
        print("Expected return: ", expected_return)
        print("Expected volatility:", expected_std)

        # optimize the weights

        constraint = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
        bound = tuple((0, 1) for x in range(len(weights)))
        res = minimize(
            Calculate().portfolio_volatility,
            np.array(
                len(weights)
                * [
                    1.0 / len(weights),
                ]
            ),
            args=(
                daily_history,
                df,
                covariance_matrix
            ),
            method="SLSQP",
            bounds=bound,
            constraints=constraint,
            tol=1e-8,
        )
        df["Optimal_Weight"] = res.x.round(6)
        optimized_weights = df["Optimal_Weight"].to_numpy()
        # TODO: Sharpe ratio should be output of calculation node Sharpe ratio.
        neg_sharpe_ratio = Calculate().portfolio_volatility(
            optimized_weights, daily_history, df, covariance_matrix
        )

        expected_return = (df["Optimal_Weight"] * df["Daily_Return"]).sum()
        expected_std = (expected_return-0.0425) / (-1*neg_sharpe_ratio)
        print("Sharpe ratio: ", -1*neg_sharpe_ratio)
        print("Expected return: ", expected_return)
        print("Expected volatility:", expected_std)
        df["Optimal_Allocation"] = (df["Optimal_Weight"] * (df["Amount"].sum())).round(
            2
        )
        return df

import pandas as pd
import numpy as np
from src.stock_calculator.calculations import Calculate
from scipy.optimize import minimize


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

        # optimize the weights
        weights = (df["Amount"] / df["Amount"].sum()).to_numpy()
        df["Original_Allocation"] = weights
        constraint = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
        bound = tuple((0, 1) for x in range(len(weights)))
        res = minimize(
            Calculate().portfolio_volatility,
            len(weights)
            * [
                1.0 / len(weights),
            ],
            args=(
                daily_history,
                df,
            ),
            method="SLSQP",
            bounds=bound,
            constraints=constraint,
        )
        df["Optimal_Weight"] = res.x

        optimized_weights = df["Optimal_Weight"].to_numpy()
        # TODO: Sharpe ratio should be output of calculation node Sharpe ratio.
        # sharpe_ratio = Calculate().portfolio_volatility(
        #    optimized_weights, daily_history, df
        # )
        df["Optimal_Allocation"] = df["Optimal_Weight"] * (df["Amount"].sum())
        return df
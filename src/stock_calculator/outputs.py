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
        df["Daily_Return"] = Calculate().returns(monthly_history, df)
        # df["Monthly_Return"] = Calculate().returns(monthly_history, df)
        # df["Quarterly_Return"] = Calculate().returns(quarterly_history, df)
        df["Volatility"] = Calculate().volatility(monthly_history, df)
        weights = (df["Amount"] / df["Amount"].sum()).to_numpy()
        df["Original_Allocation"] = weights
        sharpe_ratio = Calculate().portfolio_volatility(weights, monthly_history, df)
        expected_return = (df["Original_Allocation"] * df["Daily_Return"]).sum()
        expected_std = expected_return / (1 - sharpe_ratio)
        print("Sharpe ratio: ", 1 - sharpe_ratio)
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
                monthly_history,
                df,
            ),
            method="SLSQP",
            bounds=bound,
            constraints=constraint,
            tol=1e-8,
        )
        df["Optimal_Weight"] = res.x.round(2)
        # OUTPUTS from solver
        print("__________________")
        print(res.nit)
        print("__________________")
        optimized_weights = df["Optimal_Weight"].to_numpy()
        # TODO: Sharpe ratio should be output of calculation node Sharpe ratio.
        sharpe_ratio = Calculate().portfolio_volatility(
            optimized_weights, monthly_history, df
        )

        expected_return = (df["Optimal_Weight"] * df["Daily_Return"]).sum()
        expected_std = expected_return / (1 - sharpe_ratio)
        print("Sharpe ratio: ", 1 - sharpe_ratio)
        print("Expected return: ", expected_return)
        print("Expected volatility:", expected_std)
        df["Optimal_Allocation"] = (df["Optimal_Weight"] * (df["Amount"].sum())).round(
            2
        )
        return df

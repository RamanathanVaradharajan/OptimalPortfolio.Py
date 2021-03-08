# Run the calculator.
import sys
import copy
import pandas as pd

sys.path.append("./../../")

from src.stock_calculator.inputs import Inputs
from src.stock_calculator.yahoo_finance import YahooFinance
from src.stock_calculator.calculations import Calculate
from src.stock_calculator.outputs import Output


if __name__ == "__main__":

    input_df = Inputs().read_inputs(r"./../dataframes/input/input_portfolio.xlsx")
    print(r"Input.")
    print(input_df)

    output_df = copy.copy(input_df)
    stocks = list(input_df["Stock"])
    daily, monthly, quarterly = YahooFinance().all_history(stocks)
    output_df = Output().put_outputs(output_df, daily, monthly, quarterly)

    print(r"Output.")
    print(output_df)

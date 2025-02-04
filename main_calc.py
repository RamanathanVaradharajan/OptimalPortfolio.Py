# Run the calculator.
import copy
import pandas as pd
import sys

from src.attributes import excel_input_names as ein
from src.stock_calculator.inputs import Inputs
from src.stock_calculator.outputs import Output
from src.stock_calculator.yahoo_finance import YahooFinance
from src.stock_calculator.backtesting import BackTest


if __name__ == "__main__":

    input_df = Inputs().read_inputs(ein.filepath)

    print(r"Input.")
    print(input_df)

    output_df = copy.copy(input_df)
    stocks = list(input_df[ein.df_stock])
    daily, monthly, quarterly = YahooFinance().all_history(stocks)
    output_df = Output().put_outputs(output_df, daily, monthly, quarterly, stocks)

    print(r"Output.")

    BackTest().back_test(daily, stocks, output_df["Amount"])
    BackTest().back_test(daily, stocks, output_df["Optimal_Allocation"])

    benchmark = BackTest().daily_return(daily, stocks, output_df["Amount"])
    benchmark.name = "Benchmark"
    strategy = BackTest().daily_return(daily, stocks, output_df["Optimal_Allocation"])
    BackTest().report(benchmark=benchmark,strategy=strategy)

    print(output_df)
    output_df.to_excel(ein.outpath)
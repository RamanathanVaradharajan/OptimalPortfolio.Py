# Run the calculator.
import copy
import pandas as pd
import sys

from src.attributes import excel_input_names as ein
from src.stock_calculator.inputs import Inputs
from src.stock_calculator.outputs import Output
from src.stock_calculator.yahoo_finance import YahooFinance


# if __name__ == "__main__":
def calculator(df):
    # input_df = Inputs().read_inputs(ein.filepath)
    # override df
    data = {
        "Stock_ID": [1, 2, 3, 4],
        "Stock": ["PLTR", "AMZN", "GOOG", "TSLA" ],
        "Amount": [10277.03, 8655.62, 8324.38, 1500.72],
    }
    #input_df = pd.DataFrame(data).set_index("Stock_ID")
    input_df = df
    print(r"Input.")
    # print(input_df)

    output_df = copy.copy(input_df)
    stocks = list(input_df[ein.df_stock])
    daily, monthly, quarterly = YahooFinance().all_history(stocks)
    output_df = Output().put_outputs(output_df, daily, monthly, quarterly)

    print(r"Output.")
    # print(input_df)
    print(output_df)
    output_df.to_excel(ein.outpath)
    return output_df
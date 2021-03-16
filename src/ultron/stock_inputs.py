import pandas as pd

from src.attributes import stock_input_names as sin


class StockInputs:
    def __init__(self):
        self.location = sin.stock_df_input_file_location
        self.index = sin.stock_df_index

    def read(self) -> pd.DataFrame:
        return pd.read_excel(self.location, index_col=self.index)

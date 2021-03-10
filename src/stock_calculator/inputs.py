import pandas as pd


class Inputs:
    def read_inputs(self, location: str):
        return pd.read_excel(location, index_col="Stock_ID")

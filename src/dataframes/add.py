import pandas as pd


class AddTwoColumns:
    def calculate(self, df: pd.DataFrame, column_1: str, column_2: str) -> pd.Series:
        return df[column_1] + df[column_2]

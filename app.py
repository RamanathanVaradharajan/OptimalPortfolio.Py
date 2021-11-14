import dash
import pandas as pd
from dash import html, dash_table
from dash.dependencies import Input, Output, State
from main_calc import calculator



# create app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_excel("./src/dataframes/input/input_portfolio.xlsx")
df.set_index("Stock_ID", inplace=True)


params = ["Stock", "Amount", "Optimal_Weight", "Optimal_Allocation"]
df = pd.read_excel("./src/dataframes/input/input_portfolio.xlsx")
df.set_index("Stock_ID", inplace=True)


# app layout
app.layout = html.Div(children=[
    html.H1(children='Markowitz Modern Portfolio Optimization', style={'textAlign': 'center', 'color': '#008800'}),
    html.Br(),
    html.P(children='Input portfolio and allocation.'),
    dash_table.DataTable(
        id='portfolio',
        columns=[{"name": i, "id": i} for i in df.columns],
        data = df.to_dict("records"),
        editable=True,
        export_format='xlsx',
    ),
    html.Br(),
    dash_table.DataTable(
        id='portfolio-1',
        columns=[{"name": i, "id": i} for i in params],
        data = df.to_dict("records"),
        editable=True,
        export_format='xlsx',
    ),
    html.Button("Optimize", id='apply-button', n_clicks=0),
])


@app.callback(
    Output('portfolio-1', 'data'),
    Input('apply-button', 'n_clicks'),
    State("portfolio", "data")
)
def run_script_on_click(n_clicks, table_data):
    if not n_clicks:
        return dash.no_update

    # result = subprocess.check_output('python main_calc.py', shell=True)
    df_n = pd.DataFrame.from_dict(table_data)
    df_n["Stock_ID"] = range(len(df_n))
    df_n["Amount"] = df_n["Amount"].astype(float)
    df_n.set_index("Stock_ID", inplace=True)

    result = calculator(df_n.dropna())
    return result.to_dict("records")


if __name__ == '__main__':
    app.run_server(debug=True)
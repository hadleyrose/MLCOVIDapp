from dash import Dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_table import DataTable
import pandas as pd
from src import app


dash_app = Dash(__name__,
                server=app,
                external_stylesheets=[dbc.themes.DARKLY],
                # routes_pathname_prefix='/dash_app/',
                url_base_pathname='/dash_app/')

df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

df_small = df[:20]

table = DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df_small.columns],
    data=df_small.to_dict('records')
)

modal = html.Div(
    [
        dbc.Button("Preview Data", id="open"),
        dbc.Modal(
            [
                dbc.ModalHeader("Header"),
                dbc.ModalBody(table),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
        ),
    ]
)

dash_app.layout = dbc.Container(
    [dbc.Alert("Hello World!", color="success", dismissable=True), modal],
    className="p-5"
)


# @dash_app.callback(
#     Output("modal", "is_open"),
#     [Input("open", "n_clicks"), Input("close", "n_clicks")],
#     [State("modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open

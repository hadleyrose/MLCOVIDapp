from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash_table import DataTable
import plotly.express as px
import pandas as pd
from src import app

dash_app = Dash(__name__,
                server=app,
                external_stylesheets=[dbc.themes.DARKLY],
                # routes_pathname_prefix='/dash_app/',
                url_base_pathname='/dash_app/')

covid_df = pd.read_csv('./src/static/owid-covid-data.csv')

data_input = dbc.FormGroup(
    [
        dbc.Label("Select data", html_for="dropdown"),
        dcc.Dropdown(
            id="data_dropdown",
            options=[
                {'label': 'COVID-19 Dataset', 'value': 'covid'},
                {'label': 'Upload your own', 'value': 'upload'}
            ],
            value='covid',
            style={'color': 'rgb(230, 230, 230)'}
        )
    ]
)

# TODO: preview data option, data preview in modal?
# TODO: multi select drop down on which columns to include in plotly? one for each feature of plotly? x, y, color, etc.?
# TODO: option for prophet prediction, prophet graph
# TODO: option to generate predictions to csv
# TODO: option to do other ML and select which parts of data to use, warnings based on data type

dash_form = dbc.Col([
    html.H2('Plotly Dashboard'),
    html.H4('Data'),
    data_input
])

dash_app.layout = html.Div([
    dbc.Row(
        [dash_form,
         dbc.Col(dcc.Graph(id='data_plot'))]
    )
])


@dash_app.callback(Output('data_plot', 'figure'),
                   [Input('data_dropdown', 'value')])
def display_graph(data_dropdown):
    if data_dropdown != 'covid':  # TODO: update to be user-uploaded data graph
        fig = px.line([{'x': 1, 'y': 2, 'z': 3}])
    else:
        fig = px.line(covid_df, x='date', y='total_cases', color='location')

    return fig

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import io
from dash_table import DataTable
import plotly.express as px
import pandas as pd
from src import app

dash_app = Dash(__name__,
                server=app,
                external_stylesheets=[dbc.themes.DARKLY],
                # routes_pathname_prefix='/dash_app/',
                url_base_pathname='/dash_app/')

dash_app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            dcc.Upload(
                id='datatable-upload',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '1px', 'borderStyle': 'dashed',
                    'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                },
            )
        )
    ),
    dbc.Row(
        [dbc.Col(DataTable(id='datatable-upload-container', page_size=5,
                           style_data_conditional=[
                               {
                                   'if': {'row_index': 'odd'},
                                   'backgroundColor': 'rgb(248, 248, 248)'
                               }
                           ],
                           style_header={
                               'backgroundColor': 'rgb(230, 230, 230)',
                               'fontWeight': 'bold'
                           },
                           style_cell={
                               'color': 'black'
                           }
                           )),
         dbc.Col(dcc.Graph(id='datatable-upload-graph'))]
    )
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


@dash_app.callback([Output('datatable-upload-container', 'data'),
                    Output('datatable-upload-container', 'columns')],
                   [Input('datatable-upload', 'contents')],
                   [State('datatable-upload', 'filename')])
def update_output(contents, filename):
    if contents is None:
        return [{}], []
    df = parse_contents(contents, filename)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


@dash_app.callback(Output('datatable-upload-graph', 'figure'),
                   [Input('datatable-upload-container', 'data')])
def display_graph(rows):
    df = pd.DataFrame(rows)

    if df.empty or len(df.columns) < 1:
        fig = px.line({'x': 1, 'y': 2, 'z': 3})
    else:
        fig = px.line(df, x='date', y='total_cases', color='location')

    return fig

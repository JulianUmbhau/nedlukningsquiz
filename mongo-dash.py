# %%
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import pymongo
from pymongo import MongoClient
from pymongo import collection

import os
# %%
client = MongoClient("0.0.0.0:27017")
mydb = client["animals"]
collection = mydb.shelterA

# %%
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    html.Div(id="mongo-datatable", children=[]),

    dcc.Interval(id="interval_db", interval=86400000 * 7, n_intervals=0),

    html.Button("Save to Mongo Database", id="save-it"),
    html.Button("Add Row", id="adding-row-btn", n_clicks=0),

    html.Div(id="show-graphs", children=[]),
    html.Div(id="placeholder")

])
# %%
# Display Datatable with data from Mongo database *************************
@app.callback(Output('mongo-datatable', 'children'),
              [Input('interval_db', 'n_intervals')])
def populate_datatable(n_intervals):
    print(n_intervals)
    # Convert the Collection (table) date to a pandas DataFrame
    df = pd.DataFrame(list(collection.find()))
    #Drop the _id column generated automatically by Mongo
    df = df.iloc[:, 1:]
    print(df.head(20))

    return [
        dash_table.DataTable(
            id='my-table',
            columns=[{
                'name': x,
                'id': x,
            } for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            filter_options={"case": "sensitive"},
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_current=0,  # page number that user is on
            page_size=6,  # number of rows visible per page
            style_cell={'textAlign': 'left', 'minWidth': '100px',
                        'width': '100px', 'maxWidth': '100px'},
        )
    ]



# Add new rows to DataTable ***********************************************
@app.callback(
    Output('my-table', 'data'),
    [Input('adding-rows-btn', 'n_clicks')],
    [State('my-table', 'data'),
     State('my-table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


# Save new DataTable data to the Mongo database ***************************
@app.callback(
    Output("placeholder", "children"),
    Input("save-it", "n_clicks"),
    State("my-table", "data"),
    prevent_initial_call=True
)
def save_data(n_clicks, data):
    dff = pd.DataFrame(data)
    collection.delete_many({})
    collection.insert_many(dff.to_dict('records'))
    return ""


# Create graphs from DataTable data ***************************************
@app.callback(
    Output('show-graphs', 'children'),
    Input('my-table', 'data')
)
def add_row(data):
    df_grpah = pd.DataFrame(data)
    fig_hist1 = px.histogram(df_grpah, x='age',color="animal")
    fig_hist2 = px.histogram(df_grpah, x="neutered")
    return [
        html.Div(children=[dcc.Graph(figure=fig_hist1)], className="six columns"),
        html.Div(children=[dcc.Graph(figure=fig_hist2)], className="six columns")
    ]

# %%

load_dotenv()

port = os.environ.get('dash_port')
debug = os.environ.get('dash_debug')=="True"

if __name__ == '__main__':
    app.run_server(debug=True, port=port) # or whatever you choose

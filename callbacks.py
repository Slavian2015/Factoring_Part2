from dash.dependencies import Input, Output, State, MATCH
from app import dash_app
from dash.exceptions import PreventUpdate
import dash
import os
import pandas as pd
import sqlite3
from itertools import groupby


dash_app.config['suppress_callback_exceptions'] = True
main_path_data = os.path.abspath("./data")

def search(app: dash.Dash):
    @app.callback(

        [Output('table', 'data')],
        [Input('search_btn', 'n_clicks')],
        [State('search_box', 'value')])
    def display_output(n_clicks, value):
        if n_clicks is None:
            raise PreventUpdate
        else:
            cnx = sqlite3.connect('all.db')
            final2 = pd.read_sql_query("SELECT * FROM lost_documents", cnx)
            value = value.split()
            res = [''.join(j).strip() for sub in value for k, j in groupby(sub, str.isdigit)]
            final2 = final2[(final2['doc_seria'] == res[0]) & (final2['doc_num'] == res[1])]

            return [final2.to_dict('records')]

search(dash_app)


import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
import os
import sqlite3


main_path_data = os.path.abspath("./data")
pd.options.display.float_format = '${:.6f}'.format

########  MAIN PAGE MY  ##############

def serve_layout():
    interval = dcc.Interval(id='interval', interval=1000 * 1000, n_intervals=0)
    cnx = sqlite3.connect('all.db')
    all_data = pd.read_sql_query("SELECT * FROM lost_documents", cnx)

    layout = [interval,
              html.Div(children=[
                  dbc.Row(
                      style={"padding-left":"100px","padding-right":"100px", 'margin':"50px"},
                      children=[
                      dbc.Col(style={"width":"80%"}, children=dbc.Input(type="text", id="search_box", placeholder="CCXXXXXX  или  CC XXXXXX"),),
                      dbc.Col(style={"width":"20%"}, children=dbc.Button("ПОИСК", id="search_btn", color="info"),)
                  ]),
                  dbc.Row(style={"padding":"100px", "padding-top":"0","max-height":'75%', "overflow-Y":"scroll"},
                      children=[
                     dash_table.DataTable(
                                     id="table",
                                     data=all_data.to_dict('records'),
                                     columns=[{'id': c, 'name': c} for c in all_data.columns],
                                     page_action='native',
                                     filter_action='native',
                                     filter_query='',
                                     sort_action='native',
                                     sort_mode='multi',
                                     export_headers='display',
                                     merge_duplicate_headers=True,
                                     # style_cell_conditional=[
                                     #     {
                                     #         'if': {'column_id': c},
                                     #            'fontSize': '9px',
                                     #         'max-width':'fit-content',
                                     #         'elif': {
                                     #                   'filter': 'cash eq "balance"',
                                     #               },
                                     #               'backgroundColor': 'lightblue'
                                     #        } for c in ['regim', 'timed', 'b1', 'b2','val1', 'val2','val3', 'cash','Go',]
                                     # ],
                                     style_data_conditional=[
                                         {
                                             'if': {'row_index': 'odd'},
                                             'backgroundColor': 'rgb(248, 248, 248)'
                                         },
                                     ],
                         style_table={
                             'maxHeight': '80vh',
                             'overflowY': 'scroll',
                             'max-width': '100%',
                             'minWidth': '100%',
                         },
                         style_cell={
                             'fontSize': '10px',
                             'fontFamily': 'Open Sans',
                             'textAlign': 'center',
                             'height': '30px',
                             'maxHeight': '30px',
                             'whiteSpace': 'inherit',
                             'overflow': 'hidden',
                             'textOverflow': 'ellipsis',
                         },


                                     style_header={
                                         'fontSize': '10px',
                                         'backgroundColor': 'rgb(230, 230, 230)',
                                         'fontWeight': 'bold'
                                     })
                                         ]),
              ])]


    return layout




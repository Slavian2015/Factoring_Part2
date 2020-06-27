import dash
import dash_bootstrap_components as dbc
import flask

external_stylesheets = [dbc.themes.SOLAR]
app = flask.Flask(__name__)
dash_app = dash.Dash(__name__,url_base_pathname="/", server=app,external_stylesheets=external_stylesheets)
dash_app.title = 'Factoring'



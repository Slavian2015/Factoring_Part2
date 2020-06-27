from app import dash_app, app
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import layouts

# git push heroku master
import callbacks
#heroku logs --tail

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')])


@dash_app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return layouts.serve_layout()
    else:
        return '404'

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run(debug=False)
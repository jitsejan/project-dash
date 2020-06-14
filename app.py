# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

from jiragraphs import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.H1(children='Project overview', style={
                'textAlign': 'center',
            }),
            html.H2(children='Dashboard showing the data for the different projects.', style={
                'textAlign': 'center',
            })
        ] , className="header"),
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(jira_logo.decode()), style={
               'width': '200px',
               'margin': '0px auto',
               'display': 'block',
            })
        ]),
        dcc.Graph(
            id='example-graph',
            figure=fig_done_issues,
        ) 
    ], className="container-wide")
])

if __name__ == '__main__':
    app.run_server(debug=True)
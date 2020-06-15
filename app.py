# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

from githubgraphs import *
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
        html.H4("Issues per person", style={
            'textAlign': 'center',
        }),
        dcc.Graph(
            id='jira-issues-per-person',
            figure=fig_issues_per_person,
        ),
        dcc.Graph(
            id='jira-done-issues',
            figure=fig_done_issues,
        ),
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(github_logo.decode()), style={
               'width': '200px',
               'margin': '0px auto',
               'display': 'block',
            })
        ]),
        html.Div([
            html.Div([
                html.H4("Pull requests per person", style={
                    'textAlign': 'center',
                }),
                dcc.Graph(
                    id='github-pr-per-person',
                    figure=fig_pr_per_person           
                )], className="six columns",
            ),
            html.Div([
                html.H4("Changes per person", style={
                 'textAlign': 'center',
                }),
                dcc.Graph(
                    id='github-changes-per-person',
                    figure=fig_changes_per_person,
                )], className="six columns",
        )], className="row"),
        html.Div([
            html.Div([
                html.H4("Duration of a pull request", style={
                    'textAlign': 'center',
                }),
                dcc.Graph(
                    id='github-done-pulls',
                    figure=fig_done_pulls           
                )], className="six columns",
            ),
            html.Div([
                html.H4("Changes per pull request", style={
                 'textAlign': 'center',
                }),
                dcc.Graph(
                    id='github-changes-in-pr',
                    figure=fig_changes_in_pr,
                )], className="six columns",
        )], className="row"),
        html.Div([
            html.Div([
                html.H4("Average duration per week per PR", style={
                 'textAlign': 'center',
                }),
                dcc.Graph(
                    id='github-duration-pr-by-week',
                    figure=fig_duration_pr_by_week           
                )], className="six columns",
            ),
            html.Div([
                html.H4("Average # changes per week per PR", style={
                 'textAlign': 'center',
                }),
                dcc.Graph(
                    id='github-changes-in-pr-by-week',
                    figure=fig_changes_in_pr_by_week,
                )], className="six columns",
        )], className="row"),
    ], className="container-wide")
])

if __name__ == '__main__':
    app.run_server(debug=True)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from githubgraphs import *

layout = html.Div([
    html.Div([
        html.Img(src='assets/github.PNG', style={
            'width': '200px',
            'margin': '0px auto',
            'display': 'block',
        })
    ]),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.H4("Pull requests per person", style={
                                'textAlign': 'center',
                            }),
                            dcc.Graph(
                                id='github-pr-per-person',
                                figure=fig_pr_per_person,
                            )
                        ]
                    ), width=6, lg=6, md=6, xs=12),
                    dbc.Col(html.Div(
                        [
                            html.H4("Changes per person", style={
                                'textAlign': 'center',
                            }),
                            dcc.Graph(
                                id='github-changes-per-person',
                                figure=fig_changes_per_person,
                            )
                        ]
                    ), width=6, lg=6, md=6, xs=12),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.H4("Duration of a pull request", style={
                                'textAlign': 'center',
                            }),
                            dcc.Graph(
                                id='github-done-pulls',
                                figure=fig_done_pulls,
                            )
                        ]
                    ), width=6, lg=6, md=6, xs=12),dbc.Col(html.Div(
                        [
                            html.H4("Changes per pull request", style={
                                'textAlign': 'center',
                            }),
                            dcc.Graph(
                                id='github-changes-in-pr',
                                figure=fig_changes_in_pr,
                            )
                        ]
                    ), width=6, lg=6, md=6, xs=12),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.H4("Average duration per week per PR", style={
                                'textAlign': 'center',
                            }),
                            dcc.Graph(
                                id='github-duration-pr-by-week',
                                figure=fig_duration_pr_by_week         
                            )
                        ]
                    ), width=6, lg=6, md=6, xs=12),
                    dbc.Col(html.Div(
                        [
                            html.H4("Average # changes per week per PR", style={
                                'textAlign': 'center',
                            }),
                            dcc.Graph(
                                id='github-changes-in-pr-by-week',
                                figure=fig_changes_in_pr_by_week,
                            )
                        ]
                    ), width=6, lg=6, md=6, xs=12),
                ]
            ),
        ]
    )
])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
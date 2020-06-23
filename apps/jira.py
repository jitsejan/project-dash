import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from jiragraphs import *

layout = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src="assets/jira.PNG",
                    style={"width": "200px", "margin": "0px auto", "display": "block",},
                )
            ]
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.H4(
                                        "Issues per person",
                                        style={"textAlign": "center",},
                                    ),
                                    dcc.Graph(
                                        id="jira-issues-per-person",
                                        figure=fig_issues_per_person,
                                    ),
                                ]
                            ),
                            width=6,
                            lg=6,
                            md=6,
                            xs=12,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H4(
                                        "Done issues", style={"textAlign": "center",}
                                    ),
                                    dcc.Graph(
                                        id="jira-done-issues", figure=fig_done_issues,
                                    ),
                                ]
                            ),
                            width=6,
                            lg=6,
                            md=6,
                            xs=12,
                        ),
                    ]
                ),
            ]
        ),
    ]
)

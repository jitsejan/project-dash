import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import math

from app import app
from jiragraphs import *

colors = {
    'bug': "255, 86, 48",
    "story": "54, 179, 126",
}


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
                    dbc.Col(
                        html.Div(
                            [
                                html.H4(
                                    f"Average number of days to close a ticket", style={"textAlign": "center",}
                                ),
                                dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(
                                            [
                                               dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.H1(
                                                            f"{math.ceil(duration_stats['average'])}",  style={"textAlign": "right"}
                                                        ),
                                                        width={"size": 5, "offset": 1},
                                                    ),
                                                    dbc.Col(
                                                        html.Div(
                                                            [
                                                                "Days on average"
                                                            ]
                                                        ),
                                                        width={"size": 6},
                                                    ),
                                                ]),
                                            ]
                                        ),
                                        width=6,
                                        lg=6,
                                        md=6,
                                        xs=12,
                                    ),
                                    dbc.Col(
                                       dbc.ListGroup(
                                        [
                                            dbc.ListGroupItem(
                                                [
                                                    html.Img(
                                                        src="assets/jira_bug.SVG",
                                                        style={"width": "64px"},
                                                    ),
                                                    dbc.ListGroupItemHeading(f"{num_done['Bug']}"),
                                                    dbc.ListGroupItemText("bugs"),
                                                ]
                                            ),
                                            dbc.ListGroupItem(
                                                [
                                                    html.Img(
                                                        src="assets/jira_story.SVG",
                                                        style={"width": "64px"},
                                                    ),
                                                    dbc.ListGroupItemHeading(f"{num_done['Story']} "),
                                                    dbc.ListGroupItemText("stories"),
                                                ]
                                            ),
                                        ], horizontal=True),
                                        width=6,
                                        lg=6,
                                        md=6,
                                        xs=12,
                                    ),
                                ]),
                                dcc.Graph(
                                    id="jira-done-issues", figure=fig_done_issues,
                                )
                            ]
                        ),
                        width=12,
                        lg=12,
                        md=12,
                        xs=12,
                    )
                ),
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
                                        id="jira-done-issues-temp", figure=fig_issues_per_person,
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

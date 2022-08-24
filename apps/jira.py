import math

import dash_bootstrap_components as dbc
from dash import dcc, html

from jiragraphs import *

colors = {
    "bug": "255, 86, 48",
    "story": "54, 179, 126",
}


layout = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src="assets/jira.PNG",
                    style={
                        "width": "200px",
                        "margin": "0px auto",
                        "display": "block",
                    },
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
                                    f"Number of days to close a ticket",
                                    style={
                                        "textAlign": "center",
                                    },
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
                                                                    f"{math.ceil(duration_stats['average'])}",
                                                                ),
                                                                id="day-average",
                                                                width={
                                                                    "size": 1,
                                                                    "offset": 2,
                                                                },
                                                            ),
                                                            dbc.Col(
                                                                html.Div(
                                                                    [
                                                                        html.H1(
                                                                            "Days on average"
                                                                        ),
                                                                        html.H2(
                                                                            "From Created to Done"
                                                                        ),
                                                                    ],
                                                                    id="day-average-title",
                                                                ),
                                                                width={
                                                                    "size": 9,
                                                                    "offset": 0,
                                                                },
                                                            ),
                                                        ]
                                                    ),
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
                                                            dbc.ListGroupItemHeading(
                                                                f"{num_done['Bug'] if 'Bug' in num_done.keys() else 0}"
                                                            ),
                                                            dbc.ListGroupItemText(
                                                                "bugs"
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.ListGroupItem(
                                                        [
                                                            html.Img(
                                                                src="assets/jira_story.SVG",
                                                                style={"width": "64px"},
                                                            ),
                                                            dbc.ListGroupItemHeading(
                                                                f"{num_done['Story']} "
                                                            ),
                                                            dbc.ListGroupItemText(
                                                                "stories"
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                                horizontal=True,
                                            ),
                                            width=6,
                                            lg=6,
                                            md=6,
                                            xs=12,
                                        ),
                                    ]
                                ),
                                dcc.Graph(
                                    id="jira-done-issues",
                                    figure=fig_done_issues,
                                ),
                            ]
                        ),
                        width=12,
                        lg=12,
                        md=12,
                        xs=12,
                    )
                )
            ],
            className="graph-container",
        ),
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            [
                                html.H4(
                                    f"Days per state",
                                    style={
                                        "textAlign": "center",
                                    },
                                ),
                                dcc.Graph(
                                    id="jira-par-process",
                                    figure=fig_par_process,
                                ),
                            ]
                        ),
                        width=12,
                        lg=12,
                        md=12,
                        xs=12,
                    )
                )
            ],
            className="graph-container",
        ),
    ]
)

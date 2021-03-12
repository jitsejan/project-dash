import math

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from githubgraphs import *

try:
    duration_stats
except:
    layout = None
else:
    layout = html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src="assets/github.PNG",
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
                                        f"Number of days to close a pull request",
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
                                                                                "Day(s) on average"
                                                                            ),
                                                                            html.H2(
                                                                                "From Created to Merged"
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
                                                                    src="assets/github_pr.PNG",
                                                                    style={
                                                                        "width": "64px"
                                                                    },
                                                                ),
                                                                dbc.ListGroupItemHeading(
                                                                    f"{num_done}"
                                                                ),
                                                                dbc.ListGroupItemText(
                                                                    "pull requests"
                                                                ),
                                                            ]
                                                        ),
                                                        # dbc.ListGroupItem(
                                                        #     [
                                                        #         html.Img(
                                                        #             src="assets/jira_story.SVG",
                                                        #             style={"width": "64px"},
                                                        #         ),
                                                        #         dbc.ListGroupItemHeading(f"{num_done['Story']} "),
                                                        #         dbc.ListGroupItemText("stories"),
                                                        #     ]
                                                        # ),
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
                                        id="github-done-pulls",
                                        figure=fig_done_pulls_scatter,
                                    ),
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
                                            "Pull requests per person",
                                            style={
                                                "textAlign": "center",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="github-pr-per-person",
                                            figure=fig_pr_per_person,
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
                                            "Changes per person",
                                            style={
                                                "textAlign": "center",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="github-changes-per-person",
                                            figure=fig_changes_per_person,
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
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H4(
                                            "Duration of a pull request",
                                            style={
                                                "textAlign": "center",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="github-done-pulls",
                                            figure=fig_done_pulls,
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
                                            "Changes per pull request",
                                            style={
                                                "textAlign": "center",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="github-changes-in-pr",
                                            figure=fig_changes_in_pr,
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
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H4(
                                            "Average duration per week per PR",
                                            style={
                                                "textAlign": "center",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="github-duration-pr-by-week",
                                            figure=fig_duration_pr_by_week,
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
                                            "Average # changes per week per PR",
                                            style={
                                                "textAlign": "center",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="github-changes-in-pr-by-week",
                                            figure=fig_changes_in_pr_by_week,
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


@app.callback(
    Output("app-1-display-value", "children"), [Input("app-1-dropdown", "value")]
)
def display_value(value):
    return 'You have selected "{}"'.format(value)

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

pd.options.mode.chained_assignment = None  # default='warn'

from app import app
from apps import github, jira

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

nav_items = dbc.Container(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/", id="page-1-link")),
        dbc.NavItem(dbc.NavLink("Jira", href="/jira", id="page-2-link")),
        dbc.NavItem(dbc.NavLink("Github", href="/github", id="page-3-link")),
    ]
)
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem(dbc.NavLink("Jira Board", href="#")),
        dbc.DropdownMenuItem(dbc.NavLink("Jira Backlog", href="#")),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem(dbc.NavLink("Github Main", href="#")),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Project Dash", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav([nav_items, dropdown], className="ml-auto", navbar=True),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

layout = html.Div()
#     [
#         html.Div(
#             [
#                 html.H1(children="Project overview", style={"textAlign": "center",}),
#                 dbc.Row(
#                     [dbc.Col(html.Img(src="assets/github.PNG", className="row-img")),]
#                 ),
#                 dbc.Row([dbc.Col(github.open_pulls_table),], align="center",),
#                 dbc.Row(
#                     [dbc.Col(html.Img(src="assets/jira.PNG", className="row-img")),]
#                 ),
#                 dbc.Row(
#                     dbc.Col(
#                         html.H3(children="In progress", style={"textAlign": "center",}),
#                     ),
#                 ),
#                 dbc.Row([dbc.Col(jira.open_issues_table),], align="center",),
#                 dbc.Row(
#                     dbc.Col(
#                         html.H3(children="In review", style={"textAlign": "center",}),
#                     ),
#                 ),
#                 dbc.Row([dbc.Col(jira.review_issues_table),], align="center",),
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             html.H3(children="Todo", style={"textAlign": "center",}),
#                         ),
#                     ],
#                     align="center",
#                 ),
#                 dbc.Row([dbc.Col(jira.todo_issues_table),], align="center",),
#             ]
#         )
#     ]
# )

app.layout = dbc.Container(
    [
        navbar,
        dbc.Container(
            [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
        ),
    ],
    fluid=True,
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return layout
    elif pathname == "/jira":
        return jira.layout
    elif pathname == "/github":
        return github.layout
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


def toggle_navbar_collapse(n, is_open):
    """ Callback to toggle the collapse on small screens """
    if n:
        return not is_open
    return is_open


app.callback(
    Output(f"navbar-collapse", "is_open"),
    [Input(f"navbar-toggler", "n_clicks")],
    [State(f"navbar-collapse", "is_open")],
)(toggle_navbar_collapse)


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        return True, False, False
    elif pathname == "/jira":
        return [False, True, False]
    elif pathname == "/github":
        return [False, False, True]
    return False, False, False


app.title = "Project Dash"

if __name__ == "__main__":
    app.run_server(debug=True, port=8051)

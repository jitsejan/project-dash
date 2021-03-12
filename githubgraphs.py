""" githubgraphs.py """
import base64
from datetime import datetime

import dash_table as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

try:
    pulls = pd.read_pickle("github_pulls.df")
except:
    print("No Github to load")
else:
    pulls["changes"] = pulls["deletions"] + pulls["additions"]
    pulls["duration"] = (pulls["closed_at"] - pulls["created_at"]).dt.days

    done_pulls = pulls[pulls["closed_at"].notnull()]
    num_done = done_pulls.count()["number"]
    duration_stats = done_pulls.agg({"duration": ["average", "max", "min"]}).to_dict()[
        "duration"
    ]

    # Duration of pull requests | Scatter
    fig_done_pulls_scatter = px.scatter(
        data_frame=done_pulls,
        x="closed_at",
        y="duration",
        color="user",
        hover_data={"title"},
        size="changed_files",
        # color_discrete_map=color_discrete_map
    )
    fig_done_pulls_scatter.update_layout(
        xaxis={
            "title": "Closing date",
        },
        yaxis={
            "title": "Duration (days)",
        },
        paper_bgcolor="rgba(255,255,255,1)",
        plot_bgcolor="rgba(0,0,0,0.1)",
        legend_title_text="",
        xaxis_tickformat="%d %b <br>%Y",
    )
    fig_done_pulls_scatter.update_xaxes(
        tickangle=45,
        showgrid=True,
    )

    # Pull requests per person
    pulls_per_person = pulls.groupby("user", as_index=False).count()[["user", "title"]]
    fig_pr_per_person = go.Figure(
        data=[
            go.Pie(
                labels=pulls_per_person["user"],
                values=pulls_per_person["title"],
                textinfo="label+percent",
                insidetextorientation="radial",
                hole=0.3,
            )
        ]
    )
    fig_pr_per_person.update_layout(showlegend=False)
    # Changes per person
    pulls_per_person = pulls.groupby("user", as_index=False).sum()[["user", "changes"]]
    fig_changes_per_person = go.Figure(
        data=[
            go.Pie(
                labels=pulls_per_person["user"],
                values=pulls_per_person["changes"],
                textinfo="label+value",
                insidetextorientation="radial",
                hole=0.3,
            )
        ]
    )
    fig_changes_per_person.update_layout(showlegend=False)
    # Stats for finished pulls
    done_pulls = pulls[pulls["closed_at"].notnull()]
    fig_done_pulls = px.bar(
        done_pulls, x="number", y="duration", color="user", hover_data={"title"}
    )
    fig_done_pulls.update_layout(
        xaxis=dict(
            title="Pull request #",
        ),
        yaxis=dict(
            title="Closing time [hours]",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # Changes per pull request
    fig_changes_in_pr = px.bar(
        pulls, x="number", y="changes", color="user", hover_data={"title"}
    )
    fig_changes_in_pr.update_layout(
        xaxis=dict(
            title="Pull request #",
        ),
        yaxis=dict(
            title="Number of changes",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # Average duration per week
    mean_duration = (
        pulls.groupby([pd.Grouper(key="closed_at", freq="W-MON")])["duration"]
        .mean()
        .reset_index()
    )
    mean_duration["week"] = mean_duration["closed_at"].dt.strftime("%W")
    fig_duration_pr_by_week = px.line(mean_duration, x="week", y="duration")
    fig_duration_pr_by_week.update_layout(
        xaxis=dict(
            title="Week #",
            dtick=1,
        ),
        yaxis=dict(
            title="Duration [hour]",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig_duration_pr_by_week.update_traces(mode="markers+lines")

    # Average changes per week
    mean_pulls = (
        pulls.groupby([pd.Grouper(key="created_at", freq="W-MON")])["changes"]
        .mean()
        .reset_index()
    )
    mean_pulls["week"] = mean_pulls["created_at"].dt.strftime("%W")

    fig_changes_in_pr_by_week = px.line(mean_pulls, x="week", y="changes")
    fig_changes_in_pr_by_week.update_layout(
        xaxis=dict(title="Week #", dtick=1),
        yaxis=dict(
            title="Number of changes",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig_changes_in_pr_by_week.update_traces(mode="markers+lines")

    # Tables
    def get_table(dataframe):
        return dt.DataTable(
            columns=[
                {"name": i, "id": i, "deletable": False} for i in dataframe.columns
            ],
            data=dataframe.to_dict("records"),
            css=[
                {
                    "selector": ".dash-cell div.dash-cell-value",
                    "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;",
                }
            ],
        )

    open_filter = pulls.state == "open"
    pulls.loc[open_filter, "duration"] = datetime.now() - pulls["created_at"]
    open_pulls = pulls[open_filter][
        ["number", "title", "user", "created_at", "duration"]
    ]
    open_pulls_table = get_table(open_pulls)

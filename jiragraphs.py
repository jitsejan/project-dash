""" jiragraphs.py """
import base64
from datetime import datetime

from dash import dash_table as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytz

color_discrete_map = {"Bug": "rgb(255, 86, 48)", "Story": "rgb(54, 179, 126)"}

preffont = dict(
    size=10,
    # color=colors['graphtext']
)
issues = pd.read_pickle("jira_issues.df")
# Issues per person overall
issues_per_person = issues.groupby("assignee", as_index=False).count()[
    ["assignee", "key"]
]
fig_issues_per_person = px.pie(issues_per_person, values="key", names="assignee")
fig_issues_per_person.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=preffont
)

# Stats for finished issues
done_issues = issues[(issues["status"] == "Done") & (issues["assignee"].notnull())]
done_issues["estimate"].fillna(1, inplace=True)
done_issues.loc[:, ["duration"]] = (
    done_issues["updated"] - done_issues["created"]
).dt.days

done_issues = done_issues[done_issues["assignee"] != ""][
    [
        "updated",
        "sprint",
        "id",
        "key",
        "summary",
        "assignee",
        "duration",
        "issuetype",
        "estimate",
    ]
].sort_values("id")
fig_done_issues = px.bar(
    done_issues,
    x="duration",
    y="key",
    hover_data={"summary"},
    # orientation="h",
)
fig_done_issues.update_layout(
    xaxis=dict(
        title="Duration (days)",
    ),
    yaxis=dict(
        title="Ticket",
        autorange="reversed",
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=preffont,
)

num_done = done_issues.groupby("issuetype").count()["key"].to_dict()
duration_stats = done_issues.agg({"duration": ["average", "max", "min"]}).to_dict()[
    "duration"
]
done_issues["estimate"] = done_issues["estimate"].astype("float")
fig_done_issues = px.scatter(
    data_frame=done_issues,
    x="updated",
    y="duration",
    color="issuetype",
    hover_data={"summary"},
    size="estimate",
    color_discrete_map=color_discrete_map,
)
fig_done_issues.update_layout(
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
fig_done_issues.update_xaxes(
    tickangle=45,
    showgrid=True,
)
total_fig = px.scatter(done_issues, x="updated", y="duration", trendline="lowess")
x = total_fig["data"][1]["x"]  # * 1000
y = total_fig["data"][1]["y"]
fig_done_issues.add_trace(go.Scatter(x=x, y=y, name=f"Avg #days combined"))

grouped_fig = px.scatter(
    done_issues, x="updated", y="duration", color="issuetype", trendline="lowess"
)
for group in grouped_fig["data"]:
    if not isinstance(group["x"][0], datetime):
        x = group["x"] * 1000
        y = group["y"]
        fig_done_issues.add_trace(
            go.Scatter(x=x, y=y, name=f"Avg #days for {group['name']}")
        )


def get_table(dataframe):
    return dt.DataTable(
        columns=[{"name": i, "id": i, "deletable": False} for i in dataframe.columns],
        data=dataframe.to_dict("records"),
        css=[
            {
                "selector": ".dash-cell div.dash-cell-value",
                "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;",
            }
        ],
    )


open_filter = (issues.status == "In Progress") & (issues.issuetype == "Story")
issues.loc[open_filter, "duration"] = datetime.now(pytz.utc) - issues["updated"]
open_issues = issues[open_filter][["key", "assignee", "updated", "duration"]]
open_issues_table = get_table(open_issues)

review_filter = (issues.status == "In Review") & (issues.issuetype == "Story")
issues.loc[review_filter, "duration"] = datetime.now(pytz.utc) - issues["updated"]
review_issues = issues[review_filter][["key", "assignee", "updated", "duration"]]
review_issues_table = get_table(review_issues)

todo_filter = (issues.status == "To Do") & (issues.issuetype == "Story")
issues.loc[todo_filter, "duration"] = datetime.now(pytz.utc) - issues["updated"]
todo_issues = issues[todo_filter][["key", "assignee", "updated", "duration"]]
todo_issues_table = get_table(todo_issues)

# Parallel coordinates
# --------------------
# Normalize the historical data
hdf = pd.json_normalize(
    issues["histories"]
    .apply(pd.Series)
    .stack()
    .to_frame("histories")
    .reset_index(level=0)
    .rename(columns={"level_0": "index"})
    .to_dict(orient="records")
).set_index("index")

hdf = hdf[hdf["histories.old"] != hdf["histories.new"]]
hdf = issues.join(hdf).drop("histories", axis=1)
# Add transition column
hdf["transition"] = hdf["histories.old"] + "-" + hdf["histories.new"]
# Add the Created column as additional transition
cdf = hdf[["key", "created"]]
hdf.loc[:, "histories.created"] = pd.to_datetime(hdf["histories.created"], utc=True)
cdf.loc[:, "histories.created"] = pd.to_datetime(cdf["created"], utc=True)
cdf.loc[:, ["transition"]] = "Created"
cdf.drop("created", axis=1, inplace=True)
# Combine the two transition frames
tdf = hdf[["key", "histories.created", "transition"]]
tdf = pd.concat([tdf, cdf])
tdf.dropna(subset=["histories.created"], inplace=True)
tdf["histories.created"] = pd.to_datetime(tdf["histories.created"], utc=True)
tdf.drop_duplicates(["key", "transition"], inplace=True)
# Pivot the data and calculate the three states
pdf = tdf.pivot(index="key", values="histories.created", columns="transition")
mask = (
    pdf["In Progress-Testing"].notnull()
    & pdf["To Do-In Progress"].notnull()
    & pdf["In Progress-Testing"].notnull()
)
mdf = pdf[mask]
mdf.loc[:, "in_todo"] = mdf["To Do-In Progress"] - mdf["Created"]
mdf.loc[:, "in_progress"] = mdf["In Progress-Testing"] - mdf["To Do-In Progress"]
mdf.loc[:, "in_review"] = mdf["Testing-Done"] - mdf["In Progress-Testing"]
# Select columns
mdf = mdf[["in_todo", "in_progress", "in_review"]]
# Convert timedeltas to days
mdf = mdf.applymap(lambda x: x.days)
mdf.reset_index(inplace=True)
# Add issuetype to table
mdf = mdf.join(hdf[["issuetype"]]).drop_duplicates()
# Add is_bug boolean to table
mdf["is_bug"] = mdf["issuetype"] == "Bug"
# Calculate the min and max values
rmin = mdf[["in_todo", "in_progress", "in_review"]].values.min()
rmax = mdf[["in_todo", "in_progress", "in_review"]].values.max()

fig_par_process = go.Figure(
    data=go.Parcoords(
        line=dict(
            color=mdf["is_bug"],
            colorscale=[[0, "rgb(54, 179, 126)"], [1, "rgb(255, 86, 48)"]],
        ),
        dimensions=list(
            [
                dict(range=[rmin, rmax], label="Todo", values=mdf["in_todo"]),
                dict(
                    range=[rmin, rmax], label="In progress", values=mdf["in_progress"]
                ),
                dict(range=[rmin, rmax], label="In review", values=mdf["in_review"]),
            ]
        ),
    )
)

""" jiragraphs.py """
import base64
from datetime import datetime

import dash_table as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

color_discrete_map = {
    'Bug': 'rgb(255, 86, 48)',
    'Story': 'rgb(54, 179, 126)'}

preffont = dict(
    size=10,
    # color=colors['graphtext']
)
issues = pd.read_pickle("jira_issues.df")

# Issues per person overall
issues_per_person = issues.groupby("assignee_displayname", as_index=False).count()[
    ["assignee_displayname", "key"]
]
fig_issues_per_person = px.pie(
    issues_per_person, values="key", names="assignee_displayname"
)
fig_issues_per_person.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=preffont
)

# Stats for finished issues
done_issues = issues[ (issues['status_name'] == 'Done') & (issues["assignee_displayname"].notnull())]
done_issues['estimate'].fillna(1, inplace=True)
done_issues["duration"] = (done_issues["updated"] - done_issues["created"]).dt.days
# done_issues = done_issues[done_issues["assignee_displayname"] != ""][
#     ["sprint_name", "id", "key", "summary", "assignee_displayname", "duration"]
# ].sort_values("id")
# fig_done_issues = px.bar(
#     done_issues,
#     x="duration",
#     y="key",
#     hover_data={"summary"},
#     # orientation="h",  
# )
# fig_done_issues.update_layout(
#     xaxis=dict(title="Duration (days)",),
#     yaxis=dict(title="Ticket", autorange="reversed",),
#     paper_bgcolor="rgba(0,0,0,0)",
#     plot_bgcolor="rgba(0,0,0,0)",
#     font=preffont,
# )

num_done = done_issues.groupby("issuetype_name").count()['key'].to_dict()
duration_stats = done_issues.agg({'duration': ['average', 'max', 'min']}).to_dict()['duration']

fig_done_issues = px.scatter(
    data_frame=done_issues,
    x="updated",
    y="duration",
    color="issuetype_name",
    hover_data={"summary"},
    size="estimate",
    color_discrete_map=color_discrete_map
)
fig_done_issues.update_layout(
    xaxis={
        'title': "Closing date",
    },
    yaxis={
        'title': "Duration (days)",
    },
    paper_bgcolor="rgba(255,255,255,1)",
    plot_bgcolor="rgba(0,0,0,0.1)",
    legend_title_text='',
    xaxis_tickformat = '%d %b <br>%Y',
)
fig_done_issues.update_xaxes(
    tickangle=45,
     showgrid=True,
)
total_fig = px.scatter(done_issues, x="updated", y="duration", trendline="lowess")
x = total_fig['data'][1]['x'] * 1000
y = total_fig['data'][1]['y']
fig_done_issues.add_trace(go.Scatter(x=x, y=y, name=f"Avg #days combined"))

grouped_fig = px.scatter(done_issues, x="updated", y="duration", color="issuetype_name", trendline="lowess")
for group in grouped_fig['data']:
    if not isinstance(group['x'][0], datetime):
        x = group['x'] * 1000
        y = group['y']
        fig_done_issues.add_trace(go.Scatter(x=x, y=y, name=f"Avg #days for {group['name']}"))


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


open_filter = (issues.status_name == "In Progress") & (issues.issuetype_name == "Story")
issues.loc[open_filter, "duration"] = datetime.now() - issues["updated"]
open_issues = issues[open_filter][
    ["key", "assignee_displayname", "updated", "duration"]
]
open_issues_table = get_table(open_issues)

review_filter = (issues.status_name == "In Review") & (issues.issuetype_name == "Story")
issues.loc[review_filter, "duration"] = datetime.now() - issues["updated"]
review_issues = issues[review_filter][
    ["key", "assignee_displayname", "updated", "duration"]
]
review_issues_table = get_table(review_issues)

todo_filter = (issues.status_name == "To Do") & (issues.issuetype_name == "Story")
issues.loc[todo_filter, "duration"] = datetime.now() - issues["updated"]
todo_issues = issues[todo_filter][
    ["key", "assignee_displayname", "updated", "duration"]
]
todo_issues_table = get_table(todo_issues)

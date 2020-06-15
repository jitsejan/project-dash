""" jiragraphs.py """
import base64
import pandas as pd
import plotly.express as px

image_filename = 'images/jira.PNG'
jira_logo = base64.b64encode(open(image_filename, 'rb').read())

colors = dict(
    # graphtext='rgb(242, 158, 57)'
)
preffont = dict(
    size=10,
    # color=colors['graphtext']
)
issues = pd.read_pickle("jira_issues.df")

# Issues per person overall
issues_per_person = issues.groupby("assignee_displayname", as_index=False).count()[['assignee_displayname', 'key']]
fig_issues_per_person = px.pie(issues_per_person, values='key', names='assignee_displayname')
fig_issues_per_person.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=preffont
)

# Stats for finished issues
done_issues = issues[issues.status_name == "Done"].fillna("")
done_issues['duration'] = (done_issues['updated'] - done_issues['created']).dt.days
done_issues = done_issues[done_issues['assignee_displayname'] != ""][['sprint_name', 'id', 'key', 'summary', 'assignee_displayname', 'duration']].sort_values('id')
fig_done_issues = px.bar(done_issues, x="duration", y='key', color="assignee_displayname", hover_data={'summary'}, orientation='h')
fig_done_issues.update_layout(
    xaxis=dict(
        title='Duration (days)',
    ),
    yaxis=dict(
        title='Ticket',
        autorange='reversed',
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=preffont
)
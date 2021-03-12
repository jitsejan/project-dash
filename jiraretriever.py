""" jira.py """
import base64
import json
import os

import pandas as pd
import requests
from jira import JIRA


class JiraRetriever:
    SELECT_COLS = [
        "project_key",
        "sprint_name",
        "priority_name",
        "key",
        "id",
        "summary",
        "description",
        "resolution",
        "estimate",
        "assignee_displayname",
        "creator_displayname",
        "reporter_displayname",
        "issuetype_name",
        "duedate",
        "status_name",
        "created",
        "updated",
        "history",
    ]

    def __init__(self, board_id=None, project=None):
        self._board_id = board_id
        self._project = project
        self._jira = self._get_jira_client()

    def get_projects(self):
        return self.jira.projects()

    def get_issues_dataframe(self):
        df = self._get_frame_from_issues(self._get_issues_for_project())
        timecols = ["created", "updated"]
        df[timecols] = df[timecols].apply(
            lambda col: pd.to_datetime(col, errors="ignore", utc=True)
        )
        print(df.dtypes)
        return df

    def get_sprints_dataframe(self):
        return pd.DataFrame(self._get_sprints_for_board_id())

    def _get_sprints_for_board_id(self, board_id=None):
        sprint_info = []
        for sprint in self.jira.sprints(
            board_id=board_id if board_id else self.board_id
        ):
            sprint_info.append(
                self.jira.sprint_info(board_id=board_id, sprint_id=sprint.id)
            )
        return sprint_info

    @staticmethod
    def _get_history_for_issue(histories):
        changes = []
        for history in histories:
            for item in history.get("items"):
                if item.get("field") == "status":
                    changes.append(
                        {
                            "from": item.get("fromString"),
                            "to": item.get("toString"),
                            "date": history.get("created"),
                        }
                    )
        return changes

    def _get_issues_for_project(self, project=None):
        return self.jira.search_issues(
            f"project={project if project else self.project}",
            maxResults=None,
            expand="changelog",
        )

    def _get_issues_for_sprint(self, sprint):
        return self.jira.search_issues(f"Sprint = '{sprint}'")

    def _get_issue_with_changelog(self, issue):
        return self.jira.issue(issue=issue, expand="changelog")

    def _get_jira_client(self):
        return JIRA(self.url, basic_auth=(self.user, self.password))

    def _get_frame_from_issues(self, issues):
        data = [i.__dict__.get("raw") for i in issues]
        df = pd.json_normalize(data=data)
        df = df.rename(
            columns={
                "fields.customfield_11715": "estimate",
                "fields.customfield_10000": "sprint",
            }
        )
        df = df[[col for col in df.columns if "customfield" not in col]]
        df.columns = [
            col.replace("fields.", "").replace(".", "_").lower() for col in df.columns
        ]
        df["history"] = df["changelog_histories"].apply(self._get_history_for_issue)
        df["sprint"] = df["sprint"].apply(lambda x: x[0] if x is not None else x)
        df["sprint_name"] = df["sprint"].str.extract(
            r"name=(?P<sprint_name>.*),startDate"
        )
        return df[self.SELECT_COLS].sort_values("id")

    @property
    def api_key(self):
        return os.getenv("JIRA_API_KEY")

    @property
    def board_id(self):
        return self._board_id

    @property
    def jira(self):
        return self._jira

    @property
    def project(self):
        return self._project

    @property
    def password(self):
        return os.getenv("JIRA_API_KEY")

    @property
    def url(self):
        return os.getenv("JIRA_URL")

    @property
    def user(self):
        return os.getenv("JIRA_USER")

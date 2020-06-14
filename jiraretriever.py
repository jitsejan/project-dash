""" jira.py """
import base64
import json
import os

import pandas as pd
import requests
from jira import JIRA


class JiraRetriever:
    ESTIMATE_FIELD = "customfield_10008"
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
    ]

    def __init__(self, board_id=None, project=None):
        self._board_id = board_id
        self._project = project
        self._jira = self._get_jira_client()

    def get_projects(self):
        return self.jira.projects()

    def get_sprints_for_board_id(self, board_id=None):
        sprint_info = []
        for sprint in self.jira.sprints(
            board_id=board_id if board_id else self.board_id
        ):
            sprint_info.append(
                self.jira.sprint_info(board_id=board_id, sprint_id=sprint.id)
            )
        return pd.DataFrame(sprint_info)

    def get_issues_for_project(self, project=None):
        issues = self.jira.search_issues(
            f"project={project if project else self.project}", maxResults=None
        )
        return self._get_frame_from_issues(issues)

    def get_issues_for_sprint(self, sprint):
        return self.jira.search_issues(f"Sprint = '{sprint}'")

    def _get_jira_client(self):
        return JIRA(self.url, basic_auth=(self.user, self.password))

    def _get_frame_from_issues(self, issues):
        data = [i.__dict__.get("raw") for i in issues]
        df = pd.json_normalize(data=data)
        df = df.rename(
            columns={
                "fields.customfield_10008": "estimate",
                "fields.customfield_10000": "sprint",
            }
        )
        df = df[[col for col in df.columns if "customfield" not in col]]
        df.columns = [
            col.replace("fields.", "").replace(".", "_").lower() for col in df.columns
        ]
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
        return os.getenv("JIRA_PASSWORD")

    @property
    def url(self):
        return os.getenv("JIRA_URL")

    @property
    def user(self):
        return os.getenv("JIRA_USER")

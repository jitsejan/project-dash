""" __main__.py """
import argparse
import json
import os

import confuse

from githubretriever import GitHubRetriever
from jiraretriever import JiraRetriever

APPNAME = "PROJECTDASH"


def get_cli():
    argp = argparse.ArgumentParser()
    argp.add_argument("-j", "--jira_retrieve", action="store_true", default=False)
    argp.add_argument("-g", "--github_retrieve", action="store_true", default=False)
    argp.add_argument("-o", "--output", action="store_true", default=False)
    args = argp.parse_args()
    return args


def get_config():
    config = confuse.Configuration(APPNAME)
    config.set_args(get_cli())
    return config


def main(config):
    if config["jira_retrieve"].get():
        retr = JiraRetriever(
            board_id=config["jira"]["board_id"].get(int),
            project=config["jira"]["project"].get(),
        )
        sprints = retr.get_sprints_dataframe()
        issues = retr.get_issues_dataframe()
        if config["output"]:
            print(issues)
            print(sprints)
    if config["github_retrieve"].get():
        retr = GitHubRetriever(
            repos=config["github"]["repos"].as_str_seq(),
        )
        branches = retr.get_branches_dataframe()
        pulls = retr.get_pulls_dataframe()
        if config["output"]:
            print(branches)
            print(pulls)


if __name__ == "__main__":
    config = get_config()
    main(config)

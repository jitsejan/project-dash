""" __main__.py """
import argparse
import json
import os

import confuse

from jiraretriever import JiraRetriever

APPNAME = "PROJECTDASH"


def get_cli():
    argp = argparse.ArgumentParser()
    argp.add_argument("-o", "--output", action="store_true", default=False)
    args = argp.parse_args()
    return args


def get_config():
    config = confuse.Configuration(APPNAME)
    config.set_args(get_cli())
    return config


def main(config):
    retr = JiraRetriever(
        board_id=config["jira"]["board_id"].get(int),
        project=config["jira"]["project"].get(),
    )
    if config["output"]:
        print(retr.get_sprints_for_board_id())
        print(retr.get_issues_for_project())


if __name__ == "__main__":
    config = get_config()
    main(config)

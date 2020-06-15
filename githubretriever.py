""" githubretriever """
import pandas as pd
import os
from github import Github


class GitHubRetriever:

    def __init__(self, repos: list = []):
        self._repos = repos
        self._git = self._get_github_client()

    def get_branches_dataframe(self):
        return pd.DataFrame(self._get_branches_for_all_repos())

    def get_pulls_dataframe(self):
        dataframe = pd.DataFrame(self._get_pulls_for_all_repos())
        dataframe['number'] = dataframe['number'].astype('str')
        return dataframe

    def _get_branches_for_all_repos(self):
        branches = []
        for repo_name in self.repos:
            repo = self._get_repo(repo_name=repo_name)
            branches.extend(self._get_branches_for_repo(repo))
        return branches
            
    def _get_branches_for_repo(self, repo):
        for branch in repo.get_branches():
            yield {
                "repo_name": repo.name,
                "branch_name": branch.name,
            }

    def _get_pulls_for_all_repos(self):
        pulls = []
        for repo_name in self.repos:
            repo = self._get_repo(repo_name=repo_name)
            pulls.extend(self._get_pulls_for_repo(repo))
        return pulls

    def _get_pulls_for_repo(self, repo):
        for pull in repo.get_pulls(state="all"):
            yield {
                "number": pull.number,
                "title": pull.title,
                "state": pull.state,
                "created_at": pull.created_at,
                "updated_at": pull.updated_at,
                "closed_at": pull.closed_at,
                "merged_at": pull.merged_at,
                "user": pull.user.login,
                "comments": pull.comments,
                "review_comments": pull.review_comments,
                "commits": pull.commits,
                "additions": pull.additions,
                "deletions": pull.deletions,
                "changed_files": pull.changed_files,
            }

    def _get_github_client(self):
        return Github(self.token)

    def _get_repo(self, repo_name: str):
        return self.git.get_repo(repo_name)
    
    @property
    def git(self):
        return self._git

    @property
    def repos(self):
        return self._repos

    @property
    def token(self):
        return os.getenv("GITHUB_TOKEN")

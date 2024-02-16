from typing import Tuple

import requests

from explain_pr.providers.github.pull_request_data import PullRequestData
from explain_pr.providers.github.pull_request_analytics import PullRequestAnalytics


class GitHubProvider:
    BASE_URL = "https://api.github.com"
    BASE_HEADERS = {
        "Accept": "application/vnd.github.v3+json"
    }
    DEFAULT_TIMEOUT = 60  # seconds

    def get_pull_request_data(self, owner: str, repository: str, pr_number: int) -> \
            Tuple[PullRequestData, PullRequestAnalytics]:  # noqa: E501

        print(f"> Getting data for https://github.com/{owner}/{repository}/pull/{pr_number}/")

        title, description = self._get_pr_details(owner, repository, pr_number)
        commit_messages = self._get_commit_messages(owner, repository, pr_number)
        file_changes = self._get_file_changes(owner, repository, pr_number)

        pr_data = PullRequestData(title, description, commit_messages, file_changes)

        pr_analytics = self._calculate_analytics(pr_data)

        return pr_data, pr_analytics

    def _get_pr_details(self, owner: str, repository: str, pr_number: int):
        # https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#get-a-pull-request
        # Get pull request details
        response = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repository}/pulls/{pr_number}",
            headers=self.BASE_HEADERS,
            timeout=self.DEFAULT_TIMEOUT
        )
        pr_data = response.json()

        return pr_data["title"], pr_data["body"]

    def _get_commit_messages(self, owner: str, repository: str, pr_number: int):
        response = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repository}/pulls/{pr_number}/commits",
            headers=self.BASE_HEADERS,
            timeout=self.DEFAULT_TIMEOUT
        )
        commits_data = response.json()

        return [commit["commit"]["message"] for commit in commits_data]

    def _get_file_changes(self, owner: str, repository: str, pr_number: int):
        response = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repository}/pulls/{pr_number}/files",
            headers=self.BASE_HEADERS,
            timeout=self.DEFAULT_TIMEOUT
        )
        changes_data = response.json()

        return [
            {
                # includes relative path
                "filename": file["filename"],
                "status": file["status"],
                "changes_patch": file["patch"],
                "count_additions": file["additions"],
                "count_deletions": file["deletions"],
                "count_changes": file["changes"]

            } for file in changes_data
        ]

    def _calculate_analytics(self, pr_data: PullRequestData):
        title_size = len(pr_data.title)
        description_size = len(pr_data.description)
        commit_messages_size = [len(commit) for commit in pr_data.commit_messages]
        file_changes_size = [
            {
                "filename_size": len(file["filename"]),
                "status_size": len(file["status"]),
                "changes_patch_size": len(file["changes_patch"]),
                "total_size": len(file["filename"]) + len(file["status"]) + len(file["changes_patch"])
            } for file in pr_data.file_changes
        ]

        return PullRequestAnalytics(title_size, description_size, commit_messages_size, file_changes_size)

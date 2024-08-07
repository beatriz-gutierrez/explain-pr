from typing import Tuple, Dict, List, Union

import requests
import hashlib

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
        files_changes = self._get_commit_changes(owner, repository, pr_number)

        pr_data = PullRequestData(title, description, commit_messages, files_changes)
        pr_analytics = self._calculate_analytics(pr_data)

        return pr_data, pr_analytics

    def _get_pr_details(self, owner: str, repository: str, pr_number: int) -> Tuple[str, str]:
        # https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#get-a-pull-request
        # Get pull request details
        response = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repository}/pulls/{pr_number}",
            headers=self.BASE_HEADERS,
            timeout=self.DEFAULT_TIMEOUT
        )
        pr_data = response.json()
        return pr_data["title"], pr_data["body"]

    def _get_commit_messages(self, owner: str, repository: str, pr_number: int) -> Dict[str, str]:
        response = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repository}/pulls/{pr_number}/commits",
            headers=self.BASE_HEADERS,
            timeout=self.DEFAULT_TIMEOUT
        )
        commits_data = response.json()
        return {
            commit["sha"]: commit["commit"]["message"]
            for commit in commits_data
        }

    def _get_commit_changes(
        self, owner: str, repository: str, pr_number: int
    ) -> Dict[str, Dict[str, Union[str, int]]]:
        response = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repository}/pulls/{pr_number}/files",
            headers=self.BASE_HEADERS,
            timeout=self.DEFAULT_TIMEOUT
        )
        changes_data = response.json()
        return {
            file["sha"]:
            {
                # includes relative path
                "filename": file["filename"],
                "status": file["status"],
                "changes_patch": file["patch"] if "patch" in file else "",
                "count_additions": file["additions"],
                "count_deletions": file["deletions"],
                "count_changes": file["changes"]

            } for file in changes_data
        }

    def _calculate_analytics(self, pr_data: PullRequestData) -> PullRequestAnalytics:
        title_size = len(pr_data.title)
        description_size = len(pr_data.description)
        commit_messages_size = {key: len(value) for key, value in pr_data.commit_messages.items()} 

        files_changes_size = {}
        for key, value in pr_data.files_changes.items():
            files_changes_size[key] = {
                "filename_size": len(value["filename"]),
                "status_size": len(value["status"]),
                "changes_patch_size": len(value["changes_patch"]),
                "total_size": (
                    len(value["filename"])
                    + len(value["status"])
                    + len(value["changes_patch"])
                ),
            }

        return PullRequestAnalytics(title_size, 
                                    description_size, 
                                    commit_messages_size, 
                                    files_changes_size)

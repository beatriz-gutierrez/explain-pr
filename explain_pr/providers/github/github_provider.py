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
        commit_changes = self._get_commit_changes(owner, repository, pr_number)

        pr_data = PullRequestData(title, description, commit_messages, commit_changes)
        breakpoint()
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
    ) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        response = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repository}/pulls/{pr_number}/files",
            headers=self.BASE_HEADERS,
            timeout=self.DEFAULT_TIMEOUT
        )
        changes_data = response.json()
        breakpoint()
        return {
            file["sha"]:
            {
                # includes relative path
                "filename": file["filename"],
                "status": file["status"],
                "changes_patch": file["patch"],
                "count_additions": file["additions"],
                "count_deletions": file["deletions"],
                "count_changes": file["changes"]

            } for file in changes_data
        }

    def _calculate_analytics(self, pr_data: PullRequestData) -> PullRequestAnalytics:
        title_size = len(pr_data.title)
        description_size = len(pr_data.description)
        commit_messages_size = {key: len(value) for key, value in pr_data.commit_messages.items()} 

        commit_changes_size = {}
        for key, value in pr_data.commit_changes.items():
            for file in value:
                breakpoint()
                file_analytics = {}
                file_analytics["commit_sha"] = key
                file_analytics["filename"] = file["filename"]
                file_analytics["filename_size"] = len(file["filename"])
                file_analytics["status_size"] = len(file["status"])
                file_analytics["changes_patch_size"] = len(file["changes_patch"])
                file_analytics["total_size"] = len(file["filename"]) + len(file["status"]) + len(file["changes_patch"])

                hash_key = hashlib.sha256(key.encode() + file["filename"].encode()).hexdigest()
                commit_changes_size[hash_key] = file_analytics

        return PullRequestAnalytics(title_size, description_size, commit_messages_size, commit_changes_size)

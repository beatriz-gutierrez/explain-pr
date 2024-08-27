import pytest
from unittest.mock import MagicMock
from requests import get
import os
import sys
from explain_pr.providers.github.github_provider import GitHubProvider
from explain_pr.providers.github.pull_request_data import PullRequestData

class TestGitHubProvider:

    @pytest.fixture(autouse=True)
    def setup_function(self, mock_url):
        self.mock_request_get = MagicMock(spec=get)

        self.mock_request_get.url = (
            mock_url
        )
        self.mock_request_get.headers = {}
        self.mock_request_get.timeout = 0
        # data = {
        #     "title": "title", 
        #     "body": "description", 
        #     "commit_messages": {
        #         "commit1_sha": "commit_message1", 
        #         "commit2_sha": "commit_message2"
        #     }, 
        #     "files_changes": {
        #         "file1_sha": {
        #             "filename": "README.md", 
        #             "status": "modified", 
        #             "changes_patch": "----", 
        #             "count_additions": 0, 
        #             "count_deletions": 1, 
        #             "count_changes": 1
        #         }, 
        #         "file2_sha": {
        #             "filename": ".gitignore", 
        #             "status": "modified", 
        #             "changes_patch": "----", 
        #             "count_additions": 0, 
        #             "count_deletions": 1, 
        #             "count_changes": 1
        #         }
        #     }
        # }
        # self.mock_request_get.json.return_value = PullRequestData(
        #         title=f"{data['title']}", 
        #         body=f"{data['body']}", 
        #         commit_messages=f"{data['commit_messages']}",
        #         files_changes=f"{data['files_changes']}"
        # )
        # analytics = {
        #     "title_size": len(data["title"]),
        #     "description_size": len(data["body"]),
        #     "commit_messages_size": {key: len(value) for key, value in data["commit_messages"].items()},
        #     "files_changes_size": {}
        # }
    

    @pytest.fixture(autouse=True)
    def teardown_function(self):
        self.mock_request_get.reset_mock()


    def test_get_pull_requestr_data_with_valid_pr_number(self):
        # Arrange
        git_provider = GitHubProvider()
        urls = [
            "https://api.github.com/repos/owner/repository/pulls/1",
            "https://api.github.com/repos/owner/repository/pulls/1/commits",
            "https://api.github.com/repos/owner/repository/pulls/1/files",
        ]
        self.mock_request_get.side_effect = [MagicMock(url=MagicMock(return_value=url_i)) for url_i in urls]
        
        # Act
        pr_data, pr_analytics = git_provider.get_pull_request_data(
            "owner", "repository", 1
        )

        # Assert
        assert pr_data.title == self.mock_requests_get.json()["title"]
        assert pr_data.description == self.mock_requests_get.json()["body"]
        self.mock_requests_get.assert_called_once_with(
            self.mock_url,
            headers=self.mock_requests_get.headers,
            timeout=self.mock_requests_get.timeout,
        )
        assert pr_data.commit_messages == self.mock_requests_get.json()["commit_messages"]
        assert pr_data.files_changes == self.mock_requests_get.json()["files_changes"]


# def test_get_pr_details_with_valid_pr_number(mock_requests_get):
#     # Arrange
#     git_provider = GitHubProvider()

#     # Act
#     response_title, response_body = git_provider._get_pr_details(
#         "owner", "repository", 1
#     )

#     # Assert
#     assert response_title == mock_requests_get.json()["title"]
#     assert response_body == mock_requests_get.json()["body"]
#     mock_requests_get.assert_called_once_with(
#         "https://api.github.com/repos/owner/repository/pulls/1",
#         headers=mock_requests_get.headers,
#         timeout=mock_requests_get.timeout,
#     )

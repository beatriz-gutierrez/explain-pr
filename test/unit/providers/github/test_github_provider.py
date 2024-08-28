import pytest
from unittest.mock import MagicMock, patch
from requests import get
import sys
import os


print("PATH1", os.path.abspath(os.path.join(os.path.dirname(__file__))))
print("PATH2", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))
# Add the root directory of the project to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
from explain_pr.providers.github.github_provider import GitHubProvider


class TestGitHubProvider:

    @pytest.fixture(autouse=True)
    def setup_function(self):
        self.mock_request_get = patch("requests.get").start()

        responses = [
            MagicMock(
                json=MagicMock(
                    return_value={"title": "PR Title", "body": "PR Description"}
                ),
            ),
            MagicMock(
                json=MagicMock(
                    return_value=[
                        {
                            "sha": "123",
                            "commit": {"message": "commit_message1"},
                        },
                        {
                            "sha": "456",
                            "commit": {"message": "commit_message2"},
                        },
                    ]
                )
            ),
            MagicMock(
                json=MagicMock(
                    return_value=[
                        {
                            "sha": "123",
                            "filename": "README.md",
                            "status": "modified",
                            "additions": 0,
                            "deletions": 1,
                            "changes": 1,
                            "patch": "----",
                        },
                            "sha": "456",
                            "filename": ".gitignore",
                            "status": "modified",
                            "additions": 0,
                            "deletions": 1,
                            "changes": 1,
                            "patch": "--------",
                        },
                    ]
                )
            ),
        ]
        
        self.mock_request_get.side_effect = responses

    @pytest.fixture(autouse=True)
    def teardown_function(self):
        self.mock_request_get.reset_mock()

    def test_get_pull_requestr_data_with_valid_pr_number(self):
        # Arrange
        git_provider = GitHubProvider()
        expected_urls = [
            "https://api.github.com/repos/owner1/repository1/pulls/1",
            "https://api.github.com/repos/owner1/repository1/pulls/1/commits",
            "https://api.github.com/repos/owner1/repository1/pulls/1/files",
        ]

        # Act
        pr_data, pr_analytics = git_provider.get_pull_request_data(
            "owner1", "repository1", 1
        )

        # Assert
        assert pr_data.title == "PR Title"
        assert pr_data.description == "PR Description"
        assert pr_data.commit_messages == {
            "commit1_sha": "commit_message1",
            "commit2_sha": "commit_message2",
        }
        assert pr_data.files_changes == {
            "file1_sha": {
                "filename": "README.md",
                "status": "modified",
                "changes_patch": "----",
                "count_additions": 0,
                "count_deletions": 1,
                "count_changes": 1,
            },
            "file2_sha": {
                "filename": ".gitignore",
                "status": "modified",
                "changes_patch": "--------",
                "count_additions": 0,
                "count_deletions": 1,
                "count_changes": 1,
            },
        }
        assert self.mock_request_get.call_count == 3
        self.mock_request_get.assert_any_call(expected_urls[0])
        self.mock_request_get.assert_any_call(expected_urls[1])
        self.mock_request_get.assert_any_call(expected_urls[2])
        assert pr_analytics.title_size == len("PR Title")
        assert pr_analytics.description_size == len("PR Description")
        assert pr_analytics.commit_messages_size == {
            "commit1_sha": 15,
            "commit2_sha": 15,
        }
        assert pr_analytics.files_changes_size == {
            "file_x_sha": {
                "filename_size": 9,
                "status_size": 8,
                "changes_patch_size": 4,
                "total_size": 21,
            },
            "file_y_sha": {
                "filename_size": 13,
                "status_size": 8,
                "changes_patch_size": 8,
                "total_size": 29,
            },
        }

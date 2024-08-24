import pytest
from unittest.mock import patch, MagicMock
from explain_pr.providers.github.pull_request_data import PullRequestData
from explain_pr.providers.github.pull_request_analytics import PullRequestAnalytics
from explain_pr.adapters.adjusted_pull_request_for_llm import adjust_patch_data_size

class TestAdjustedPullRequestForLlm:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.mock_pull_request_data = MagicMock(spec=PullRequestData)
        self.mock_pull_request_data.title = "Mock PR Title"
        self.mock_pull_request_data.description = "Mock PR Description"
        self.mock_pull_request_data.commit_messages = {
            "mock_commit_sha_1": "Mock Commit Message 1",
            "mock_commit_sha_2": "Mock Commit Message 2",
        }
        self.mock_pull_request_data.files_changes = {
            "mock_file_sha_1": {
                "filename": "Mock File 1",
                "status": "modified",
                "changes_patch": "----",
                "count_additions": 0,
                "count_deletions": 1,
                "count_changes": 1,
            },
            "mock_file_sha_2": {
                "filename": "Mock File 2",
                "status": "modified",
                "changes_patch": "----",
                "count_additions": 0,
                "count_deletions": 1,
                "count_changes": 1,
            },
        }

        self.mock_pull_request_analytics = MagicMock(spec=PullRequestAnalytics)
        self.mock_pull_request_analytics.title_size = 16
        self.mock_pull_request_analytics.description_size = 38
        self.mock_pull_request_analytics.commit_messages_size = {
            "mock_commit_sha_1": 13,
            "mock_commit_sha_2": 24,
        }
        self.mock_pull_request_analytics.files_changes_size = {
            "mock_file_sha_1": {
                "filename_size": 9,
                "status_size": 8,
                "changes_patch_size": 5255554,
                "total_size": 500000000,
            },
            "mock_file_sha_2": {
                "filename_size": 13,
                "status_size": 2,
                "changes_patch_size": 66666661444,
                "total_size": 200000000000,
            },
        }

    @pytest.fixture(autouse=True)
    def teardown_method(self):
        # clear any call history and reset any return values or side effects
        # set during the test
        self.mock_pull_request_data.reset_mock()
        self.mock_pull_request_analytics.reset_mock()

    def test_adjust_patch_data_size_with_pr_smaller_than_limit(self):
        # ARRANGE
        max_tokens = 10000

        # ACT
        result = adjust_patch_data_size(
            self.mock_pull_request_data, self.mock_pull_request_analytics, max_tokens
        )

        # ASSERT
        assert result is self.mock_pull_request_data

    def test_adjust_patch_data_size_with_pr_bigger_than_limit(self):
        # ARRANGE
        max_tokens = 1
        mock_changes_path_ocurrences = len(
            [
                file
                for file in self.mock_pull_request_data.files_changes.values() if file["changes_patch"]!="" 
            ]
        )

        # ACT
        result = adjust_patch_data_size(
            self.mock_pull_request_data, self.mock_pull_request_analytics, max_tokens
        )
        print("mock_changes_path_ocurrences:", mock_changes_path_ocurrences)
        print("result.files_changes:", result.files_changes)
        print("Non-empty changes_patch count in result:", len([file for file in result.files_changes.values() if file["changes_patch"]!=""]))

        # ASSERT
        assert result is self.mock_pull_request_data
        assert result.title == self.mock_pull_request_data.title
        assert result.description == self.mock_pull_request_data.description
        assert result.commit_messages == self.mock_pull_request_data.commit_messages
        assert (
            len([file for file in result.files_changes.values() if file["changes_patch"]!=""]) 
            < mock_changes_path_ocurrences
        )

import pytest
from unittest.mock import MagicMock

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
                "changes_patch": "--------------------",
                "count_additions": 0,
                "count_deletions": 1,
                "count_changes": 1,
            },
            "mock_file_sha_2": {
                "filename": "Mock File 222",
                "status": "modified",
                "changes_patch": "----------------------------------------",
                "count_additions": 0,
                "count_deletions": 1,
                "count_changes": 1,
            },
        }

        self.mock_pull_request_analytics = MagicMock(spec=PullRequestAnalytics)
        self.mock_pull_request_analytics.title_size = len(self.mock_pull_request_data.title)
        self.mock_pull_request_analytics.description_size = len(self.mock_pull_request_data.description)
        self.mock_pull_request_analytics.commit_messages_size = {
            "mock_commit_sha_1": 21,
            "mock_commit_sha_2": 21,
        }
        self.mock_pull_request_analytics.files_changes_size = {
            "mock_file_sha_1": {
                "filename_size": 11,
                "status_size": 8,
                "changes_patch_size": 20,
                "total_size": 39,
            },
            "mock_file_sha_2": {
                "filename_size": 13,
                "status_size": 8,
                "changes_patch_size": 40,
                "total_size": 61,
            },
        }

    @pytest.fixture(autouse=True)
    def teardown_method(self):
        self.mock_pull_request_data.reset_mock()
        self.mock_pull_request_analytics.reset_mock()

    def test_adjust_patch_data_size_with_pr_smaller_than_limit_will_not_adjustt(self):
        # ARRANGE
        max_tokens = 100000

        # ACT
        result = adjust_patch_data_size(
            self.mock_pull_request_data, self.mock_pull_request_analytics, max_tokens
        )

        # ASSERT
        assert (
            len(
                [
                    file
                    for file in result.files_changes.values()
                    if file["changes_patch"] == ""
                ]
            )
            == 0
        )

    def test_adjust_patch_data_size_with_pr_bigger_than_limit_will_skip_all_changes(self):
        # ARRANGE
        max_tokens = 10

        # ACT
        result = adjust_patch_data_size(
            self.mock_pull_request_data, self.mock_pull_request_analytics, max_tokens
        )

        # ASSERT
        assert result.title == self.mock_pull_request_data.title
        assert result.description == "" 
        assert not result.commit_messages 
        assert not result.files_changes 

    def test_adjust_patch_data_size_with_pr_bigger_than_limit_will_skip_some_changes_patch(self):
        # ARRANGE
        max_tokens = 50

        # ACT
        result = adjust_patch_data_size(
            self.mock_pull_request_data, self.mock_pull_request_analytics, max_tokens
        )
        # ASSERT
        assert result.title == self.mock_pull_request_data.title
        assert result.description == self.mock_pull_request_data.description
        assert result.commit_messages == self.mock_pull_request_data.commit_messages
        assert len([file for file in result.files_changes.values() if file["changes_patch"]==""]) > 0

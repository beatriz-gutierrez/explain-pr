import math

from explain_pr.config import DEBUG
from explain_pr.providers.github.pull_request_data import PullRequestData
from explain_pr.providers.github.pull_request_analytics import PullRequestAnalytics


def _get_max_code_chars_per_context_window(n_tokens: int) -> int:
    # - 1 token is 2.5 characters for diffs and code
    return math.floor(n_tokens * 2.5)


def _get_remaining_tokens_per_context_window(chars_used: int, chars_per_token: int, max_tokens: int) -> int:
    return max_tokens - math.floor(chars_used / chars_per_token)


def adjust_patch_data_size(
        pr_data: PullRequestData, pr_analytics: PullRequestAnalytics, max_tokens: int) -> PullRequestData:
    size_per_text = (
        pr_analytics.title_size
        + pr_analytics.description_size
        + sum(pr_analytics.commit_messages_size.values())
    )

    code_size = sum(
        [
            file["total_size"]
            for file in pr_analytics.files_changes_size.values()
        ]
    )

    remaining_tokens = _get_remaining_tokens_per_context_window(size_per_text, 4, max_tokens)
    # if PR so big, leave only title
    if remaining_tokens <= 0:
        remaining_tokens = 0
        pr_data.description = ""
        pr_data.commit_messages = []
        pr_data.commit_changes = []
        print("> Adjusting patch data size -> removing description, commit messages and file changes.")
        return pr_data

    remaining_max_code_size = _get_max_code_chars_per_context_window(remaining_tokens)
    if DEBUG:
        print(f"CODE SIZE: {code_size} REMAINING MAX CODE SIZE: {remaining_max_code_size}")

    # order in descending order for start removing from zero index
    sorted_pr_analytics = dict(
        sorted(
            pr_analytics.files_changes_size.items(),
            key=lambda x: x[1]["changes_patch_size"],
            reverse=True
        )
    )
    pr_analytics.files_changes_size = sorted_pr_analytics

    remove_index = 0
    # order by bigger size and remove until fits
    while (
        code_size > remaining_max_code_size and remove_index < len(pr_analytics.files_changes_size)
    ):
        # remove the k-v pair of the biggest file change
        file_to_remove, file_to_remove_size = list(pr_analytics.files_changes_size.items())[remove_index]
        pr_data.files_changes[file_to_remove]["changes_patch"] = ""
        code_size -= file_to_remove_size["changes_patch_size"]

        pr_analytics.files_changes_size[file_to_remove]["changes_patch_size"] = 0
        remove_index += 1

        if DEBUG:
            print(f"CODE SIZE: {code_size} REMAINING MAX CODE SIZE: {remaining_max_code_size}")

    return pr_data

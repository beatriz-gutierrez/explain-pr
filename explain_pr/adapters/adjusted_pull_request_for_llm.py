from explain_pr.providers.github.pull_request_data import PullRequestData
from explain_pr.providers.github.pull_request_analytics import PullRequestAnalytics
from explain_pr.providers.chatgpt.chatggp_provider import MAX_TOKENS

def get_max_code_chars_per_context_window(n_tokens: int = MAX_TOKENS) -> int:
    # - 1 token is 2.5 characters for diffs and code
    return n_tokens * 2.5


def get_max_text_chars_per_context_window(n_tokens: int = MAX_TOKENS) -> int:
    # - 1 token is 4 characters for English text
    return n_tokens * 4


def get_remaining_tokens_per_context_window(chars_used: int, chars_per_token: int) -> int:
      return MAX_TOKENS - (chars_used / chars_per_token)


def adjust_patch_data_size(
    pr_data: PullRequestData, pr_analytics: PullRequestAnalytics
) -> PullRequestData:
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

    remaining_tokens = get_remaining_tokens_per_context_window(size_per_text, 4)
    # if PR so big, leave only title
    if remaining_tokens <= 0:
        remaining_tokens = 0
        pr_data.description = ""
        pr_data.commit_messages = []
        pr_data.commit_changes = []
        print("> Adjusting patch data size -> removing description, commit messages and file changes.")
        return pr_data

    remaining_max_code_size = get_max_code_chars_per_context_window(remaining_tokens)

    # order in acending order (to remove from dict easier)
    sorted_pr_analytics = dict(
        sorted(
            pr_analytics.files_changes_size.items(),
            key=lambda x: x[1]["total_size"],
        )
    )
    pr_analytics.files_changes_size = sorted_pr_analytics
    # order by bigger size and remove until fits
    while (
        code_size > remaining_max_code_size and len(pr_analytics.files_changes_size) > 0
    ):
        # remove the k-v pair of the biggest file change
        file_to_remove, file_to_remove_size  = pr_analytics.files_changes_size.popitem()
        pr_data.files_changes.pop(file_to_remove)
        code_size -= file_to_remove_size["total_size"]

    return pr_data

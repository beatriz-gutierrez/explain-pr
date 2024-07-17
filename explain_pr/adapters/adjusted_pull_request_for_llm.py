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

    size_per_code = sum(
        [
            file["total_size"]
            for files in pr_analytics.commit_changes_size.values()
            for file in files
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

    remaining_code_size = get_max_code_chars_per_context_window(remaining_tokens)

    sorted_pr_analytics = dict(
        sorted(
            pr_analytics.commit_changes_size.items(),
            key=lambda x: sum(file["total_size"] for file in x[1]),
            reverse=True,
        )
    )
    breakpoint()
    # TODO: use tehe sorted_pr_analytics to remove the biggest files first
    # example:
    # {'1db8463ece966d5188632197195abe231eee8aaf': [{'filename_size': 18, 'status_size': 5, 'changes_patch_size': 9456, 'total_size': 9479}], 'e15f19b36e0ab4e2ee348beba05208f4233a1a0c': [{'filename_size': 20, 'status_size': 5, 'changes_patch_size': 3507, 'total_size': 3532}], 'd906357919fa3521e7f0f8967916765f4651566f': [{'filename_size': 15, 'status_size': 8, 'changes_patch_size': 3501, 'total_size': 3524}], '734d1598202e36a10b2f19d4d8271d6c2f93bcd8': [{'filename_size': 11, 'status_size': 8, 'changes_patch_size': 1079, 'total_size': 1098}], '85c8b8ce894b67502c8a8b1969c352dcbcca1eed': [{'filename_size': 10, 'status_size': 8, 'changes_patch_size': 766, 'total_size': 784}], 'f3c43d5257d2b2b3e66927c718dcaff66ebe7292': [{'filename_size': 16, 'status_size': 8, 'changes_patch_size': 539, 'total_size': 563}], '6aed9d8e16c766e147054da1d527bb56a6b2d33f': [{'filename_size': 9, 'status_size': 8, 'changes_patch_size': 524, 'total_size': 541}], '04d3a1679c5573f65a0f326f49aed1585eaf0831': [{'filename_size': 25, 'status_size': 8, 'changes_patch_size': 199, 'total_size': 232}], '80fb0d0d5eb754b5df01f9f7cdf5297e0e240515': [{'filename_size': 14, 'status_size': 8, 'changes_patch_size': 189, 'total_size': 211}]}

    if size_per_code > remaining_code_size:
        # order by bigger size and remove until fits
        for file_change, file_change_size in zip(pr_data.commit_changes, pr_analytics.commit_changes_size):
            print("> Adjusting patch data size -> removing 'total_size' in file changes.")

            pr_data.commit_changes[file_change]['changes_patch'] = ''
            size_per_code -= file_change_size["total_size"]
            if size_per_code < remaining_code_size:
                return pr_data

    return pr_data

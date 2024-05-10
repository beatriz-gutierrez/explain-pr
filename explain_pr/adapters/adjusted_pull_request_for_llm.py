from explain_pr.providers.github.pull_request_data import PullRequestData
from explain_pr.providers.github.pull_request_analytics import PullRequestAnalytics
from explain_pr.providers.chatgpt.chatggp_provider import MAX_TOKENS

def get_max_code_per_context_window(n_tokens: int = MAX_TOKENS) -> int:
    # - 1 token is 2.5 characters for diffs and code
    return n_tokens * 2.5


def get_max_text_per_context_window(n_tokens: int = MAX_TOKENS) -> int:
    # - 1 token is 4 characters for English text
    return n_tokens * 4


def get_remaining_tokens_per_context_window(chars_used: int) -> int:
  def get_remaining_tokens_per_context_window(chars_used: int, chars_per_token: int) -> int:
      return MAX_TOKENS - (chars_used / chars_per_token)


def adjust_patch_data_size(
    pr_data: PullRequestData, pr_analytics: PullRequestAnalytics
) -> PullRequestData:
    size_per_text = (
        pr_analytics.title_size
        + pr_analytics.description_size
        + sum(pr_analytics.commit_messages_size)
    )
    size_per_code = sum([file["total_size"] for file in pr_analytics.file_changes_size])

    remain_tokens = get_remaining_tokens_per_context_window(size_per_text)  
    # if PR so big, leave only title
    if remain_tokens <= 0:
        remain_tokens = 0
        pr_data.description = ""
        pr_data.commit_messages = []
        pr_data.file_changes = []
        print("> Adjusting patch data size -> removing description, commit messages and file changes.")
        return pr_data

    remain_code_size = get_max_code_per_context_window(remain_tokens)
    # sorted_pr_analytics = sorted(
    #     pr_analytics.file_changes_size, key=lambda x: x["total_size"], reverse=True
    # )
    if size_per_code > remain_code_size:
        # order by bigger size and remove until fits
        for file_change, file_change_size in zip(pr_data.file_changes, pr_analytics.file_changes_size):
            print("> Adjusting patch data size -> removing 'total_size' in file changes.")

            pr_data.file_changes[file_change]['changes_patch'] = ''
            size_per_code -= file_change_size["total_size"]
            if size_per_code < remain_code_size:
                return pr_data
           
    return pr_data

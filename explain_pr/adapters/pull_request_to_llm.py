import openai
from config import OPENAI_API_KEY

from explain_pr.providers.github.pull_request_data import PullRequestData
from explain_pr.providers.github.pull_request_analytics import PullRequestAnalytics
from explain_pr.providers.chatgpt.pull_request_summary import get_pull_request_summary

MAX_CHARS = 40000  # Context window of 16000 tokens and 1 token per 2.5 characters


def summarize_pull_request(
    pr_data: PullRequestData, pr_analytics: PullRequestAnalytics
) -> str:
    openai.api_key = OPENAI_API_KEY

    # check size and reducie if more than MAX_CHARS
    adjusted_pr_data = adjust_patch_data_size(pr_data, pr_analytics)

    pull_request_content = f"""
                            title": {adjusted_pr_data.title}, 
                            "description": {adjusted_pr_data.description},
                            "commit_messages": {adjusted_pr_data.commit_messages},
                            "file_changes": {adjusted_pr_data.file_changes},
                            """
    return get_pull_request_summary(pull_request_content)


def adjust_patch_data_size(
    pr_data: PullRequestData, pr_analytics: PullRequestAnalytics
) -> PullRequestData:
    total_size = (
        pr_analytics.title_size
        + pr_analytics.description_size
        + sum(pr_analytics.commit_messages_size)
        + sum([file["total_size"] for file in pr_analytics.file_changes_size])
    )

    # if total size is greater than the max characters -> the changes_patch info is removed
    if (total_size // MAX_CHARS) > 1:
        print("> Adjusting patch data size -> removing changes_patch info")
        pr_data.file_changes = [
            {k: v if k != "changes_patch" else [] for k, v in changes.items()}
            for changes in pr_data.file_changes
        ]

    return pr_data

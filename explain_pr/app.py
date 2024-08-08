import openai

from explain_pr.config import OPENAI_API_KEY
from explain_pr.providers.github.pull_request_data import PullRequestData
from explain_pr.providers.github.pull_request_analytics import PullRequestAnalytics
from explain_pr.providers.chatgpt.chatggp_provider import get_pull_request_summary
from explain_pr.adapters.adjusted_pull_request_for_llm import adjust_patch_data_size


openai.api_key = OPENAI_API_KEY


def summarize_pull_request(
    pr_data: PullRequestData, pr_analytics: PullRequestAnalytics, max_tokens: int
) -> str:

    # check size and reduce if more than MAX_CHARS
    adjusted_pr_data = adjust_patch_data_size(pr_data, pr_analytics, max_tokens)

    pull_request_content = f"""
                            title": {adjusted_pr_data.title},
                            "description": {adjusted_pr_data.description},
                            "commit_messages": {adjusted_pr_data.commit_messages},
                            "files_changes": {adjusted_pr_data.files_changes},
                            """
    return get_pull_request_summary(pull_request_content)

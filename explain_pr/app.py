import sys

import openai

# Only performing the check for existing config file here, as this is the main application entry point
try:
    from explain_pr.config import DEBUG, OPENAI_API_KEY
except Exception as e:
    print(f"Could not find the `config.py` file inside `explain_pr` folder. More details: {e}")
    print("Please follow the README instructions to create one.")
    sys.exit(1)

from explain_pr.adapters.adjusted_pull_request_for_llm import adjust_patch_data_size
from explain_pr.adapters.markdown_to_html import markdown_to_html
from explain_pr.providers.chatgpt.chatggp_provider import get_pull_request_summary
from explain_pr.providers.github.pull_request_analytics import PullRequestAnalytics
from explain_pr.providers.github.pull_request_data import PullRequestData

openai.api_key = OPENAI_API_KEY


def summarize_pull_request(
    pr_data: PullRequestData,
    pr_analytics: PullRequestAnalytics,
    pr_url: str,
    max_tokens: int,
) -> str | None:

    # check size and reduce if more than MAX_CHARS
    adjusted_pr_data = adjust_patch_data_size(pr_data, pr_analytics, max_tokens)

    pull_request_content = f"""
                            title": {adjusted_pr_data.title},
                            "description": {adjusted_pr_data.description},
                            "commit_messages": {adjusted_pr_data.commit_messages},
                            "files_changes": {adjusted_pr_data.files_changes},
                            """

    summary = get_pull_request_summary(pull_request_content)

    return _convert_and_save_summary(summary, pr_url, adjusted_pr_data.title)


def _convert_and_save_summary(summary: str, pr_url: str, title: str) -> str | None:
    summary_html = markdown_to_html(summary, pr_url, title)

    filename = "summary"

    if DEBUG:
        with open(f"{filename}.md", "wt", encoding="utf-8") as file_handle:
            file_handle.write(summary)

    output_filename = f"{filename}.html"
    with open(output_filename, "wt", encoding="utf-8") as file_handle:
        file_handle.write(summary_html)

    return output_filename

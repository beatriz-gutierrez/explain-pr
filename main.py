import sys

from explain_pr.providers.github.github_provider import GitHubProvider
from explain_pr.app import summarize_pull_request
from explain_pr.providers.chatgpt.chatggp_provider import MAX_TOKENS


def main(repo_owner: str, repo_name: str, pull_request_number: int, max_tokens: int):
    gh_provider = GitHubProvider()
    pr_data, pr_analytics = gh_provider.get_pull_request_data(
        repo_owner, repo_name, pull_request_number)

    print(f"Title: {pr_data.title}")
    print(f"Description: {pr_data.description}")

    pr_url = f"https://github.com/{repo_owner}/{repo_name}/pull/{pull_request_number}"

    print("Do you want to summarize the pull request? (y/n)")
    answer = input()
    if answer.lower() == "y":
        print("Summarizing pull request...")
        summary_file = summarize_pull_request(pr_data, pr_analytics, pr_url, max_tokens)
        print(f"Summary saved to `{summary_file}`")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python main.py <repo_owner> <repo_name> <pull_request_number> (<max_tokens>)")
        sys.exit(1)

    arg_max_tokens = int(sys.argv[4]) if len(sys.argv) == 5 else MAX_TOKENS
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), arg_max_tokens)

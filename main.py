import sys

from explain_pr.providers.github.github_provider import GitHubProvider
from explain_pr.app import summarize_pull_request


def main(repo_owner: str, repo_name: str, pull_request_number: int):
    gh_provider = GitHubProvider()
    pr_data, pr_analytics = gh_provider.get_pull_request_data(
        repo_owner, repo_name, pull_request_number)

    print(f"Title: {pr_data.title}")
    print(f"Description: {pr_data.description}")

    print("Do you want to summarize the pull request? (y/n)")
    answer = input()
    if answer.lower() == "y":
        print("Summarizing pull request")
        summary = summarize_pull_request(pr_data, pr_analytics)
        print(summary)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python main.py <repo_owner> <repo_name> <pull_request_number>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))

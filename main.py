# import json
from math import (ceil, floor)
from typing import Dict

import requests

# percentage
TRESHOLD_FOR_ALL_PATCHES = 90

# TODO: supply via parameter
# source: https://platform.openai.com/tokenizer
# 4 characters per token for normal text; 2.5 for code and diffs
CHARS_PER_TOKEN = 2.5
# gpt-3.5-turbo-0125
MAX_TOKENS = 16385

MAX_TOKENS_FOR_ALL_PATCHES = floor(TRESHOLD_FOR_ALL_PATCHES * MAX_TOKENS / 100)


def _count_all_patch_tokens(all_file_changes: Dict):
    total_tokens = 0

    tokens_per_file = {}

    for file_changes in all_file_changes:
        filename = file_changes['filename']
        tokens_per_file[filename] = ceil(len(file_changes['patch']) / CHARS_PER_TOKEN)
        total_tokens += tokens_per_file[filename]

    return total_tokens, tokens_per_file


def _file_changes(file_changes: Dict, can_have_full_patch: bool):
    data = f"Filename:{file_changes['filename']}\nStatus:{file_changes['status']}\n"

    if can_have_full_patch:
        data += f"Changes patch: {file_changes['patch']}"
    else:
        data += f"Lines added:{file_changes['additions']}\n"
        data += f"Lines deleted:{file_changes['deletions']}\n"
        data += f"Lines changed:{file_changes['changes']}"

    return data


def get_pull_request_data(owner: str, repository: str, pr_number: int):
    base_url = "https://api.github.com"
    headers = {"Accept": "application/vnd.github.v3+json"}

    print(f"> Getting data for https://github.com/{owner}/{repository}/pull/{pr_number}/")

    # Get pull request details
    response = requests.get(
        f"{base_url}/repos/{owner}/{repository}/pulls/{pr_number}",
        headers=headers,
        timeout=60
    )
    pr_data = response.json()

    title = pr_data["title"]
    description = pr_data["body"]

    response = requests.get(
        f"{base_url}/repos/{owner}/{repository}/pulls/{pr_number}/commits",
        headers=headers,
        timeout=60
    )
    commits_data = response.json()

    commit_messages = [commit["commit"]["message"] for commit in commits_data]

    # Get file changes
    response = requests.get(
        f"{base_url}/repos/{owner}/{repository}/pulls/{pr_number}/files",
        headers=headers,
        timeout=60
    )
    files_data = response.json()

    total_tokens, tokens_per_file = _count_all_patch_tokens(files_data)
    full_patches = total_tokens <= MAX_TOKENS_FOR_ALL_PATCHES

    print(f"> Max. tokens: {MAX_TOKENS}")
    print(f"> Max. tokens for all patches: {MAX_TOKENS_FOR_ALL_PATCHES} ({TRESHOLD_FOR_ALL_PATCHES}%)")
    print(f"> Total tokens: {total_tokens}")
    print(f"> Tokens per file: {', '.join([f'{k}: {v}' for k, v in tokens_per_file.items()])}")

    file_changes = [_file_changes(file, full_patches) for file in files_data]

    return title, description, commit_messages, file_changes


if __name__ == "__main__":
    # TODO: read from args
    repo_owner = "Kartones"
    repo_name = "fg-viewer"
    pull_request_number = 24

    print(get_pull_request_data(repo_owner, repo_name, pull_request_number))

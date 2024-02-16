from dataclasses import dataclass
from typing import (List, Dict)


@dataclass
class PullRequestAnalytics:
    title_size: int
    description_size: int
    commit_messages_size: List[int]
    file_changes_size: List[Dict[str, str]]

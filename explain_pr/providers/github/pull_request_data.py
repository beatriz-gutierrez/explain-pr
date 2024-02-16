from dataclasses import dataclass
from typing import (List, Dict, Union)


@dataclass
class PullRequestData:
    title: str
    description: str
    commit_messages: List[str]
    file_changes: List[Dict[str, Union[str, int]]]

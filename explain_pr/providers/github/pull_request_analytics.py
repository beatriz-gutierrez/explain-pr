from dataclasses import dataclass
from typing import (List, Dict)


@dataclass
class PullRequestAnalytics:
    title_size: int
    description_size: int

    commit_messages_size: Dict[str, int]  # key: commit_id and value: commit_size
    file_changes_size: Dict[str, List[Dict[str, int]]] # key1: commit_id

    #  format of file_changes_size=
    #       [
    #           {
    #               'filename': 'README.md',
    #               'filename_size': 9,
    #               'status_size': 8,
    #               'changes_patch_size': 524,
    #               'total_size': 5 n n nn41
    #           },
    #           ...
    #       ]



from dataclasses import dataclass
from typing import (List, Dict)


@dataclass
class PullRequestAnalytics:
    title_size: int
    description_size: int
    commit_messages_size: List[int]

    file_changes_size: List[Dict[str, int]] 
    #  format of file_changes_size=
    #       [
    #           {
    #               'filename_size': 9, 
    #               'status_size': 8, 
    #               'changes_patch_size': 524, 
    #               'total_size': 541
    #           }, 
    #           ...
    #       ]

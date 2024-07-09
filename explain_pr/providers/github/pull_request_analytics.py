from dataclasses import dataclass
from typing import (List, Dict)

"""
Format of PullRequestAnalytics:
{
    'title_size': 16,
    'description_size': 13,
    'commit_messages_size': {
        'commit_id1': 13,
        'commit_id2': 13,
        ...
    },
    'file_changes_size': {
        'commit_id1': [
            {
                'filename': 'README.md',
                'filename_size': 9,
                'status_size': 8,
                'changes_patch_size': 524,
                'total_size': 5 n n nn41
            },
            ...
        ],
        'commit_id2': [
            {
                'filename': 'README.md',
                'filename_size': 9,
                'status_size': 8,
                'changes_patch_size': 524,
                'total_size': 5 n n nn41
            },
            ...
        ],
        ...
    }
}


"""
@dataclass
class PullRequestAnalytics:
    title_size: int
    description_size: int

    commit_messages_size: Dict[str, int] 
    file_changes_size: Dict[str, List[Dict[str, int]]] 
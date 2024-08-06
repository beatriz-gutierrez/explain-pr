from dataclasses import dataclass
from typing import (List, Dict)

# id -> sha256(commit_sha + filename)
#       commit_sha
#       filename

"""
Format of PullRequestAnalytics:
{
    'title_size': 16,
    'description_size': 13,
    'commit_messages_size': {
        'commit1_sha': 13,
        'commit2_sha': 13,
        ...
    },
    'files_changes_size': {
        'file_x_sha': 
            {
                #'filename': 'filename_y',
                'filename_size': 9,
                'status_size': 8,
                'changes_patch_size': 524,
                'total_size': 5
            },
        'file_y_sha': 
            {
                #'filename': 'filename_y',
                'filename_size': 9,
                'status_size': 8,
                'changes_patch_size': 524,
                'total_size': 5
            },
        ...
    }
}

"""
@dataclass
class PullRequestAnalytics:
    title_size: int
    description_size: int

    commit_messages_size: Dict[str, int] 
    files_changes_size: Dict[str, Dict[str, int]] 

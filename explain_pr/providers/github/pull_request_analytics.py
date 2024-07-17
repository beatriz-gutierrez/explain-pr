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
    'commit_changes_size': {
        'commit_i_filename_x_sha': 
            {
                'commit_sha': 'commit_i_sha',
                'filename': 'filename_y',
                'filename_size': 9,
                'status_size': 8,
                'changes_patch_size': 524,
                'total_size': 5
            },
        'commit_i_filename_y_sha': 
            {
                'commit_sha': 'commit_i_sha',
                'filename': 'filename_y',
                'filename_size': 9,
                'status_size': 8,
                'changes_patch_size': 524,
                'total_size': 5
            },
        'commit_j_filename_x_sha': 
            {
                'commit_sha': 'commit_i_sha',
                'filename': 'filename_y',
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
    commit_changes_size: Dict[str, Dict[str, int]] 

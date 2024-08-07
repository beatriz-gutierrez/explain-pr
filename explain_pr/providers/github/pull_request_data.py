from dataclasses import dataclass
from typing import Dict, Union


"""
Format of PullRequestData:
{
    'title': 'Update README.md',
    'description': 'Some description',
    'commit_messages': {
        'commit1_sha': 'commit_message1',
        'commit2_sha': 'commit_message2',
        ...
    },
    'files_changes': { # files changes in the PR
        'file1_sha': {
            'filename': 'README.md',
            'status': 'modified',
            'changes_patch': "----",
            'count_additions': 0,
            'count_deletions': 1,
            'count_changes': 1
        },
        'file2_sha': {
            'filename': '.gitignore',
            'status': 'modified',
            'changes_patch': "----",
            'count_additions': 0,
            'count_deletions': 1,
            'count_changes': 1
        },
        ...
    }
}

"""
@dataclass
class PullRequestData:
    title: str
    description: str
   
    commit_messages: Dict[str, str] 
    files_changes: Dict[str, Dict[str, Union[str, int]]]
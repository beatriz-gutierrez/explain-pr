from dataclasses import dataclass
from typing import (List, Dict, Union)


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
    'file_changes': {
        'commit1_sha': [
            {
                'filename': 'README.md',
                'status': 'modified',
                'changes_patch': "----",
                'count_additions': 0,
                'count_deletions': 1,
                'count_changes': 1
            },
            ...
        ],
        'commit2_sha': [
            {
                'filename': 'README.md',
                'status': 'modified',
                'changes_patch': "----",
                'count_additions': 0,
                'count_deletions': 1,
                'count_changes': 1
            },
            ...
        ],
        ...
    }
}

"""
@dataclass
class PullRequestData:
    title: str
    description: str
   
    commit_messages: Dict[str, str] 
    file_changes: Dict[str, List[Dict[str, Union[str, int]]]]
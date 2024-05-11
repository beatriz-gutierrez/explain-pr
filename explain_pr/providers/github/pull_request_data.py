from dataclasses import dataclass
from typing import (List, Dict, Union)


@dataclass
class PullRequestData:
    title: str
    description: str
    commit_messages: List[str]
    file_changes: List[Dict[str, Union[str, int]]]
    # format of file_changes_=
    #   [
    #       {
    #           filename': 'README.md',
    #           'status': 'modified',
    #           'changes_patch': "----',
    #           'count_additions': 0, 
    #           'count_deletions': 1, 
    #           'count_changes': 1
    #       },
    #      ...
    #   ]

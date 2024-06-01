from dataclasses import dataclass
from typing import (List, Dict, Union)


@dataclass
class PullRequestData:
    title: str
    description: str
   
    commit_messages: Dict[str, str] # key: commit_id and value: commit_message
    file_changes: Dict[str, List[Dict[str, Union[str, int]]]] # key1: commit_id
    # format of file_changes=
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

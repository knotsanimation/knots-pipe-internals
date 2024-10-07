"""
A utility library to write pipeline internals scripts.

Mostly intended to reduce **large** code duplications.
"""

__all__ = [
    "rmtree",
    "set_path_read_only",
    "backupdir",
    "gitget",
    "gitget_commit",
    "gitget_remote_url",
    "create_build_info_file",
]

from ._filesystem import rmtree
from ._filesystem import set_path_read_only
from ._filesystem import backupdir

from ._git import gitget
from ._git import gitget_commit
from ._git import gitget_remote_url

from ._buildinfo import create_build_info_file

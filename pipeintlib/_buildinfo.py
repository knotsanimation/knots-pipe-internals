import getpass
import logging
import datetime
from pathlib import Path
from typing import Optional

from ._git import gitget_commit
from ._git import gitget_remote_url

LOGGER = logging.getLogger(__name__)


def create_build_info_file(
    target_path: Path,
    git_repo: Path,
    extra_lines: Optional[list[str]] = None,
) -> str:
    """
    Create a simple file storing metadata about the current context.

    That file is intended to be human parsed for debugging so readability matter.

    Args:
        target_path: filesystem path to write the build file to. parent must exist.
        git_repo: filesystem path to a git repository to extract metadata from.
        extra_lines: list of line added to the content of the build info file.
    """
    extra_lines = extra_lines or []

    date = datetime.datetime.now()
    user = getpass.getuser()
    commit = gitget_commit(git_repo=git_repo)
    try:
        remote_url = gitget_remote_url(git_repo=git_repo)
    except Exception as error:
        # happens if no remote set
        remote_url = str(error)

    build_info = "\n".join(
        [
            f"date={date}",
            f"user={user}",
            f"commit={commit}",
            # remote is mostly added for newcomers to know where the files come from
            f"remote={remote_url}",
        ]
        + extra_lines
    )
    target_path.write_text(build_info, encoding="utf-8")
    return build_info

import subprocess
from pathlib import Path


def gitget(command: list[str], cwd: Path) -> str:
    """
    Call git and return its output.
    """
    out = subprocess.check_output(["git"] + command, cwd=cwd, text=True)
    out = out.strip("\n").strip(" ")
    return out


def gitget_commit(git_repo: Path) -> str:
    """
    Get the hash of the last commit created on the current HEAD.
    """
    git_command = ["rev-parse", "HEAD"]
    return gitget(git_command, cwd=git_repo)


def gitget_remote_url(git_repo: Path) -> str:
    """
    Get the url of the remote set in the current repository. Raise if no remote set.
    """
    git_command = ["config", "remote.origin.url"]
    return gitget(git_command, cwd=git_repo)

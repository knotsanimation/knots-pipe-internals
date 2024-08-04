import contextlib
import datetime
import getpass
import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path

THISDIR = Path(__file__).parent


def create_build_info(target_path: Path):
    git_command = ["git", "rev-parse", "HEAD"]
    commit_hash = subprocess.check_output(git_command, cwd=THISDIR, text=True)
    commit_hash = commit_hash.strip("\n")

    try:
        git_command = ["git", "config", "remote.origin.url"]
        remote_url = subprocess.check_output(git_command, cwd=THISDIR, text=True)

    except Exception as error:
        remote_url = str(error)

    build_info = "\n".join(
        [
            f"date={datetime.datetime.now()}",
            f"user={getpass.getuser()}",
            f"commit={commit_hash}",
            # remote is mostly added for beginners to know where the files come from
            f"remote={remote_url}",
        ]
    )
    target_path.write_text(build_info, encoding="utf-8")


def set_path_read_only(path: Path):
    """
    Remove write permissions for everyone on the given file without modifying other permissions.

    Reference: https://stackoverflow.com/a/38511116/13806195
    """
    # NO_USER_WRITING & NO_GROUP_WRITING & NO_OTHER_WRITING
    NO_WRITING = ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH
    current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
    os.chmod(path, current_permissions & NO_WRITING)


def rmtree(path: Path):
    # XXX: hack to avoid permission issues that even a chmod + shutil.rmtree(onerror=) can't fix
    # noinspection PyProtectedMember
    tempfile.TemporaryDirectory._rmtree(path)


@contextlib.contextmanager
def backupdir(src_dir: Path):
    """
    Delete the given directory and make a backup out of it, restored if any error happen.
    """
    backup_path = src_dir.with_stem(f"{src_dir.stem}.backup")
    print(f"creating backup '{backup_path}'")
    src_dir.rename(backup_path)
    try:
        yield
    except:
        print(f"upcomming error: reverting to backup")
        rmtree(src_dir)
        backup_path.rename(src_dir)
        raise
    else:
        print(f"removing backup '{backup_path}'")
        rmtree(backup_path)


SRC_CONFIG_PATH = THISDIR / "knots-hub.vendor-installers.json"

DST_DIR = Path(r"N:\apps\knots-hub\configs")
DST_DIR.mkdir(exist_ok=True)
DST_BUILD_INFO = DST_DIR / "deploy.info"
DST_PATHS_MAPPING = {
    SRC_CONFIG_PATH: DST_DIR / "knots-hub.vendor-installers.json",
}


with backupdir(DST_DIR):
    DST_DIR.mkdir()
    for src_path, dst_path in DST_PATHS_MAPPING.items():
        print(f"deploying '{src_path}' to '{dst_path}'")
        if src_path.is_file():
            shutil.copy2(src_path, dst_path)
        else:
            shutil.copytree(src_path, dst_path)

        print(f"setting to read-only '{dst_path}'")
        set_path_read_only(dst_path)

print(f"creating build info file at '{DST_BUILD_INFO}'")
create_build_info(target_path=DST_BUILD_INFO)
set_path_read_only(DST_BUILD_INFO)

import contextlib
import datetime
import os
import shutil
import socket
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
            f"machine={socket.gethostname()}",
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


DST_ROOT = Path(r"N:\apps\knots-hub")

SHORTCUT_SCRIPT_PATH = THISDIR / "create-windows-shortcut.ps1"
SRC_ICON_PATH = DST_ROOT / "builds" / "latest" / "icon.ico"
SRC_LAUNCHER_PATH = THISDIR / "src-launcher.bat"

DST_DIR = DST_ROOT / "launchers"
DST_DIR.mkdir(exist_ok=True)
DST_BUILD_INFO = DST_DIR / "deploy.info"
DST_LAUNCHER_PATH = DST_DIR / "knots-hub-launcher.bat"
DST_LAUNCHER_LNK_PATH = DST_ROOT / "knots-hub.lnk"

with backupdir(DST_DIR):
    DST_DIR.mkdir()
    print(f"deploying '{SRC_LAUNCHER_PATH}' to '{DST_LAUNCHER_PATH}'")
    shutil.copy2(SRC_LAUNCHER_PATH, DST_LAUNCHER_PATH)
    print(f"setting to read-only '{DST_LAUNCHER_PATH}'")
    set_path_read_only(DST_LAUNCHER_PATH)

print(f"creating build info file at '{DST_BUILD_INFO}'")
create_build_info(target_path=DST_BUILD_INFO)
set_path_read_only(DST_BUILD_INFO)

print(f"creating shortcut to '{DST_LAUNCHER_LNK_PATH}'")
DST_LAUNCHER_LNK_PATH.unlink(missing_ok=True)
subprocess.run(
    [
        "powershell.exe",
        "-NonInteractive",
        "-NoProfile",
        str(SHORTCUT_SCRIPT_PATH),
        str(DST_LAUNCHER_LNK_PATH),
        str(DST_LAUNCHER_PATH),
        "-iconPath",
        str(SRC_ICON_PATH),
    ]
)
print(f"setting to read-only: {DST_LAUNCHER_LNK_PATH}")
set_path_read_only(DST_LAUNCHER_LNK_PATH)

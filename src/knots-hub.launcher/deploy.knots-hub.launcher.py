import datetime
import os
import shutil
import socket
import stat
import subprocess
from pathlib import Path

THISDIR = Path(__file__).parent

SHORTCUT_SCRIPT_PATH = THISDIR / "create-windows-shortcut.ps1"


def add_build_info(batch_path: Path):
    content = batch_path.read_text(encoding="utf-8")
    git_command = ["git", "rev-parse", "HEAD"]
    commit_hash = subprocess.check_output(git_command, cwd=THISDIR, text=True)
    commit_hash = commit_hash.strip("\n")

    try:
        git_command = ["git", "config", "remote.origin.url"]
        remote_url = subprocess.check_output(git_command, cwd=THISDIR, text=True)
    except Exception as error:
        remote_url = str(error)

    build_info = ";".join(
        [
            f"date={datetime.datetime.now()}",
            f"machine={socket.gethostname()}",
            f"commit={commit_hash}",
            # remote is mostly added for beginners to know where the files come from
            f"remote={remote_url}",
        ]
    )
    new_content = f":: {build_info}\n{content}"
    batch_path.write_text(new_content, encoding="utf-8")


def set_path_read_only(path: Path):
    """
    Remove write permissions for everyone on the given file without modifying other permissions.

    Reference: https://stackoverflow.com/a/38511116/13806195
    """
    # NO_USER_WRITING & NO_GROUP_WRITING & NO_OTHER_WRITING
    NO_WRITING = ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH
    current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
    os.chmod(path, current_permissions & NO_WRITING)


DEPLOY_ROOT = Path(r"N:\apps\knots-hub")
SRC_LAUNCHER_PATH = THISDIR / "src-launcher.bat"
DST_LAUNCHER_DIR = DEPLOY_ROOT / "builds"
DST_LAUNCHER_PATH = DST_LAUNCHER_DIR / "knots-hub-launcher.bat"
DST_LAUNCHER_LNK_PATH = DEPLOY_ROOT / "knots-hub.lnk"
LATEST_BUILD_ICON_PATH = DEPLOY_ROOT / "builds" / "latest" / "icon.ico"

DST_LAUNCHER_DIR.mkdir(exist_ok=True)
print(f"copying '{SRC_LAUNCHER_PATH}' to '{DST_LAUNCHER_PATH}'")
shutil.copy(SRC_LAUNCHER_PATH, DST_LAUNCHER_PATH)
print("adding build info")
add_build_info(DST_LAUNCHER_PATH)
print(f"setting to read-only: {DST_LAUNCHER_PATH}")
set_path_read_only(DST_LAUNCHER_PATH)

# we create a shortcut just to add an icon and so people can easily copy it on their
# desktop while still allowing use to update the code if needed
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
        str(LATEST_BUILD_ICON_PATH),
    ]
)
print(f"setting to read-only: {DST_LAUNCHER_LNK_PATH}")
set_path_read_only(DST_LAUNCHER_LNK_PATH)

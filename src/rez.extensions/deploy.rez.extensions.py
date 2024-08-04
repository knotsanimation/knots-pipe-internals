import datetime
import os
import shutil
import socket
import stat
import subprocess
import tempfile
from pathlib import Path

THISDIR = Path(__file__).parent.resolve()


def create_build_info(target_path: Path) -> str:
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
    return build_info


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


WORKDIR = THISDIR / ".workspace"
if WORKDIR.exists():
    rmtree(WORKDIR)
WORKDIR.mkdir()

DEPLOY_ROOT = Path(r"N:\apps")
DST_EXTENSIONS_DIR = DEPLOY_ROOT / "rez" / "extensions"
DST_BUILD_INFO = DST_EXTENSIONS_DIR / "deploy.info"
SRC_REPODIR = WORKDIR / "rez_extensions"
SRC_PATHS_MAPPING = {
    SRC_REPODIR / "include": DST_EXTENSIONS_DIR / "include",
    SRC_REPODIR / "rezplugins": DST_EXTENSIONS_DIR / "rezplugins",
}

REPO_REMOTE_URL = "https://github.com/knotsanimation/rez_extensions.git"
command = ["git", "clone", REPO_REMOTE_URL, str(SRC_REPODIR)]
print(f"running '{' '.join(command)}'")
subprocess.run(command, cwd=WORKDIR)

DST_EXTENSIONS_DIR_BACKUP = DST_EXTENSIONS_DIR.with_name(
    f"{DST_EXTENSIONS_DIR.name}.backup"
)
if DST_EXTENSIONS_DIR_BACKUP.exists():
    # safety in case a previous deploy failed to clean it
    rmtree(DST_EXTENSIONS_DIR_BACKUP)
print(f"creating backup '{DST_EXTENSIONS_DIR_BACKUP}'")
DST_EXTENSIONS_DIR.rename(DST_EXTENSIONS_DIR_BACKUP)
DST_EXTENSIONS_DIR.mkdir()

try:
    for src_path, dst_path in SRC_PATHS_MAPPING.items():
        print(f"deploying '{src_path}' to '{dst_path}'")
        if src_path.is_file():
            if dst_path.exists():
                dst_path.unlink()
            shutil.copy2(src_path, dst_path)
        else:
            if dst_path.exists():
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)

        print(f"setting to read-only '{dst_path}'")
        set_path_read_only(dst_path)

except:
    # revert as it was before
    print(f"upcomming error: reverting to backup")
    rmtree(DST_EXTENSIONS_DIR)
    DST_EXTENSIONS_DIR_BACKUP.rename(DST_EXTENSIONS_DIR)
    raise

print(f"removing backup '{DST_EXTENSIONS_DIR_BACKUP}'")
rmtree(DST_EXTENSIONS_DIR_BACKUP)

print(f"creating build info file at '{DST_BUILD_INFO}'")
create_build_info(target_path=DST_BUILD_INFO)
set_path_read_only(DST_BUILD_INFO)

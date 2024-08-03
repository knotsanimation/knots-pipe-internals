import datetime
import shutil
import socket
import subprocess
from pathlib import Path
from typing import List

THISDIR = Path(__file__).parent


def create_build_info(source_files: List[Path]):
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
    for source_file in source_files:
        info_path = source_file.with_suffix(".info")
        info_path.write_text(build_info, encoding="utf-8")


SRC_CONFIG_PATH = THISDIR / "knots-hub.vendor-installers.json"

DEPLOY_ROOT = Path(r"N:\apps\knots-hub")
DST_CONFIG_DIR = DEPLOY_ROOT / "configs"
DST_CONFIG_DIR.mkdir(exist_ok=True)

print(f"copying '{SRC_CONFIG_PATH}' to '{DST_CONFIG_DIR}'")
copied = Path(shutil.copy(SRC_CONFIG_PATH, DST_CONFIG_DIR))
print("creating build info")
create_build_info([copied])

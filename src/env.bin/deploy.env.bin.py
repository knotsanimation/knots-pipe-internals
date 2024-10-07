import shutil
from pathlib import Path

import pipeintlib

THISDIR = Path(__file__).parent


DST_ROOT = Path(r"N:\env")

SRC_BIN_DIR = THISDIR / "bin"

DST_BIN_DIR = DST_ROOT / "bin"
DST_BUILD_INFO = DST_BIN_DIR / ".deploy.info"

with pipeintlib.backupdir(DST_BIN_DIR, logger=print):
    print(f"creating bin directory '{DST_BIN_DIR}'")
    shutil.copytree(SRC_BIN_DIR, DST_BIN_DIR)
    print(f"setting to read-only '{DST_BIN_DIR}'")
    for binpath in DST_BIN_DIR.glob("*"):
        pipeintlib.set_path_read_only(binpath)

print(f"creating build info file at '{DST_BUILD_INFO}'")
pipeintlib.create_build_info_file(target_path=DST_BUILD_INFO, git_repo=THISDIR)
pipeintlib.set_path_read_only(DST_BUILD_INFO)

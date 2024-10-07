import shutil
import subprocess
from pathlib import Path

import pipeintlib

THISDIR = Path(__file__).parent.resolve()


WORKDIR = THISDIR / ".workspace"
if WORKDIR.exists():
    pipeintlib.rmtree(WORKDIR)
WORKDIR.mkdir()
SRC_REPODIR = WORKDIR / "rez_extensions"

DST_DIR = Path(r"N:\apps\rez\extensions")
DST_BUILD_INFO = DST_DIR / "deploy.info"
DST_PATHS_MAPPING = {
    SRC_REPODIR / "include": DST_DIR / "include",
    SRC_REPODIR / "rezplugins": DST_DIR / "rezplugins",
}

REPO_REMOTE_URL = "https://github.com/knotsanimation/rez_extensions.git"
command = ["git", "clone", REPO_REMOTE_URL, str(SRC_REPODIR)]
print(f"running '{' '.join(command)}'")
subprocess.run(command, cwd=WORKDIR)

with pipeintlib.backupdir(DST_DIR, logger=print):
    for src_path, dst_path in DST_PATHS_MAPPING.items():
        print(f"deploying '{src_path}' to '{dst_path}'")
        if src_path.is_file():
            shutil.copy2(src_path, dst_path)
        else:
            shutil.copytree(src_path, dst_path)

        print(f"setting to read-only '{dst_path}'")
        pipeintlib.set_path_read_only(dst_path)

print(f"creating build info file at '{DST_BUILD_INFO}'")
pipeintlib.create_build_info_file(target_path=DST_BUILD_INFO, git_repo=THISDIR)
pipeintlib.set_path_read_only(DST_BUILD_INFO)

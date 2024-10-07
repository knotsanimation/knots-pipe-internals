import shutil
from pathlib import Path

import pipeintlib

THISDIR = Path(__file__).parent


DST_DIR = Path(r"N:\apps\rez\config")
DST_DIR.mkdir(exist_ok=True)
DST_BUILD_INFO = DST_DIR / "deploy.info"
DST_PATHS_MAPPING = {THISDIR / "rez.config.main.yml": DST_DIR / "rezconfig-main.yml"}


with pipeintlib.backupdir(DST_DIR, logger=print):
    DST_DIR.mkdir()
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

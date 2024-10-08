import runpy
import shutil
import sys
from pathlib import Path

import pipeintlib

THISDIR = Path(__file__).parent


DST_ROOT = Path(r"N:\env\launchers")

BUILD_SCRIPT_PATH = THISDIR / "build.env.launchers.py"
SRC_ICON_PATH = THISDIR / "knots-hub.ico"
SRC_KHUB_PS1_PATH = THISDIR / "knots-hub.ps1.bat"
SRC_KHUB_WT_PATH = THISDIR / "knots-hub.wt.bat"

DST_BUILD_INFO = DST_ROOT / "deploy.info"
DST_ICON_PATH = DST_ROOT / "icon.ico"
DST_ENV_BATCH_PATH = DST_ROOT / "setup-env.bat"
DST_ENV_POWERSHELL_PATH = DST_ROOT / "setup-env.ps1"
DST_ENV_SHELL_PATH = DST_ROOT / "setup-env.sh"
DST_KHUB_PS1_PATH = DST_ROOT / "knots-hub.ps1.bat"
DST_KHUB_WT_PATH = DST_ROOT / "knots-hub.wt.bat"

with pipeintlib.backupdir(DST_ROOT, logger=print):
    DST_ROOT.mkdir()

    print(f"copying icon to '{DST_ICON_PATH}'")
    shutil.copy(SRC_ICON_PATH, DST_ICON_PATH)

    print(f"copying launcher to '{DST_KHUB_PS1_PATH}'")
    shutil.copy(SRC_KHUB_PS1_PATH, DST_KHUB_PS1_PATH)

    print(f"copying launcher to '{DST_KHUB_WT_PATH}'")
    shutil.copy(SRC_KHUB_WT_PATH, DST_KHUB_WT_PATH)

    sys.argv = ["", "batch", str(DST_ENV_BATCH_PATH)]
    runpy.run_path(str(BUILD_SCRIPT_PATH), run_name="__main__")
    assert DST_ENV_BATCH_PATH.exists()

    sys.argv = ["", "powershell", str(DST_ENV_POWERSHELL_PATH)]
    runpy.run_path(str(BUILD_SCRIPT_PATH), run_name="__main__")
    assert DST_ENV_POWERSHELL_PATH.exists()

    sys.argv = ["", "shell", str(DST_ENV_SHELL_PATH)]
    runpy.run_path(str(BUILD_SCRIPT_PATH), run_name="__main__")
    assert DST_ENV_SHELL_PATH.exists()

    for path in DST_ROOT.glob("*"):
        print(f"setting to read-only: {path}")
        pipeintlib.set_path_read_only(path)


print(f"creating build info file at '{DST_BUILD_INFO}'")
pipeintlib.create_build_info_file(target_path=DST_BUILD_INFO, git_repo=THISDIR)
pipeintlib.set_path_read_only(DST_BUILD_INFO)

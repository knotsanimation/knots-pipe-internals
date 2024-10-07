import shutil
import subprocess
from pathlib import Path

import pipeintlib

THISDIR = Path(__file__).parent


DST_ROOT = Path(r"N:\apps\knots-hub")

SHORTCUT_SCRIPT_PATH = THISDIR / "create-windows-shortcut.ps1"
SRC_ICON_PATH = DST_ROOT / "builds" / "latest" / "icon.ico"
SRC_LAUNCHER_PATH = THISDIR / "src-launcher.bat"

DST_DIR = DST_ROOT / "launchers"
DST_DIR.mkdir(exist_ok=True)
DST_BUILD_INFO = DST_DIR / "deploy.info"
DST_LAUNCHER_PATH = DST_DIR / "knots-hub-launcher.bat"
DST_LAUNCHER_LNK_PATH = DST_ROOT / "knots-hub.lnk"

with pipeintlib.backupdir(DST_DIR, logger=print):
    DST_DIR.mkdir()
    print(f"deploying '{SRC_LAUNCHER_PATH}' to '{DST_LAUNCHER_PATH}'")
    shutil.copy2(SRC_LAUNCHER_PATH, DST_LAUNCHER_PATH)
    print(f"setting to read-only '{DST_LAUNCHER_PATH}'")
    pipeintlib.set_path_read_only(DST_LAUNCHER_PATH)

print(f"creating build info file at '{DST_BUILD_INFO}'")
pipeintlib.create_build_info_file(target_path=DST_BUILD_INFO, git_repo=THISDIR)
pipeintlib.set_path_read_only(DST_BUILD_INFO)

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
pipeintlib.set_path_read_only(DST_LAUNCHER_LNK_PATH)

import runpy
import shutil
import subprocess
import sys
from pathlib import Path

import pipeintlib

THISDIR = Path(__file__).parent


def mklnk(
    lnk_path: Path,
    target_path: str,
    icon_path: Path,
    arguments: str = "",
):
    lnk_path.unlink(missing_ok=True)
    subprocess.run(
        [
            "powershell.exe",
            "-NonInteractive",
            "-NoProfile",
            str(SHORTCUT_SCRIPT_PATH),
            str(lnk_path),
            str(target_path),
            "-arguments",
            arguments,
            "-iconPath",
            str(icon_path),
        ],
        check=True,
    )


DST_ROOT = Path(r"N:\env\launchers")

SHORTCUT_SCRIPT_PATH = THISDIR / "create-windows-shortcut.ps1"
BUILD_SCRIPT_PATH = THISDIR / "build.env.launchers.py"
SRC_ICON_PATH = THISDIR / "knots-hub.ico"

DST_BUILD_INFO = DST_ROOT / "deploy.info"
DST_ICON_PATH = DST_ROOT / "icon.ico"
DST_ENV_BATCH_PATH = DST_ROOT / "setup-env.bat"
DST_ENV_POWERSHELL_PATH = DST_ROOT / "setup-env.ps1"
DST_ENV_SHELL_PATH = DST_ROOT / "setup-env.sh"

with pipeintlib.backupdir(DST_ROOT, logger=print):
    DST_ROOT.mkdir()

    print(f"copying icon to '{DST_ICON_PATH}'")
    shutil.copy(SRC_ICON_PATH, DST_ICON_PATH)

    sys.argv = ["", "batch", str(DST_ENV_BATCH_PATH)]
    runpy.run_path(str(BUILD_SCRIPT_PATH), run_name="__main__")
    assert DST_ENV_BATCH_PATH.exists()

    sys.argv = ["", "powershell", str(DST_ENV_POWERSHELL_PATH)]
    runpy.run_path(str(BUILD_SCRIPT_PATH), run_name="__main__")
    assert DST_ENV_POWERSHELL_PATH.exists()

    sys.argv = ["", "shell", str(DST_ENV_SHELL_PATH)]
    runpy.run_path(str(BUILD_SCRIPT_PATH), run_name="__main__")
    assert DST_ENV_SHELL_PATH.exists()

    DST_LAUNCHER_LNK_PATH = DST_ROOT / "knots-hub.ps1.lnk"
    print(f"creating shortcut '{DST_LAUNCHER_LNK_PATH}'")
    mklnk(
        lnk_path=DST_LAUNCHER_LNK_PATH,
        target_path="%SystemRoot%\\system32\\WindowsPowerShell\\v1.0\\powershell.exe",
        # https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_exe
        arguments=f'"-NoExit -File `"{DST_ENV_POWERSHELL_PATH}`""',
        icon_path=DST_ICON_PATH,
    )

    DST_LAUNCHER_LNK_PATH = DST_ROOT / "knots-hub.wt.lnk"
    print(f"creating shortcut '{DST_LAUNCHER_LNK_PATH}'")
    mklnk(
        lnk_path=DST_LAUNCHER_LNK_PATH,
        target_path="%LocalAppData%\\Microsoft\\WindowsApps\\wt.exe",
        # https://learn.microsoft.com/en-gb/windows/terminal/command-line-arguments
        # https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_exe
        arguments=f'"--window 0 new-tab --title knots-hub powershell -NoExit -File `"{DST_ENV_POWERSHELL_PATH}`""',
        icon_path=DST_ICON_PATH,
    )

    for path in DST_ROOT.glob("*"):
        print(f"setting to read-only: {path}")
        pipeintlib.set_path_read_only(path)


print(f"creating build info file at '{DST_BUILD_INFO}'")
pipeintlib.create_build_info_file(target_path=DST_BUILD_INFO, git_repo=THISDIR)
pipeintlib.set_path_read_only(DST_BUILD_INFO)

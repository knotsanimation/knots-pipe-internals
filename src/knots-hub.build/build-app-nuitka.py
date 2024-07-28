import argparse
import logging
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import knots_hub
import kloch_rezenv
import kloch_kiche

THIS_DIR = Path(__file__).parent.resolve()

LOGGER = logging.getLogger(Path(__file__).stem)


def build(
    app_name: str,
    workdir: Path,
    start_script_path: Path,
    target_dir: Path = None,
    overwrite_existing: bool = True,
    icon_path: Optional[Path] = None,
):
    """
    Args:
        app_name: filename of the executable without the extension
        workdir: Working directory for nuikta, where it can dump all of its files.
        start_script_path: Filesystem path to an existing python script used to start the application.
        target_dir: optional destination directry for the executable
        overwrite_existing:
        icon_path:  Filesystem path to an existing .ico or .png file.
    """
    command = [
        # "--verbose",
        "--standalone",
        f"--output-dir={workdir}",
        f"--output-filename={app_name}",
        f"--include-package={kloch_rezenv.__name__}",
        f"--include-package={kloch_kiche.__name__}",
    ]
    # windows specific
    if icon_path:
        command += [f"--windows-icon-from-ico={icon_path}"]

    # always last
    command += [start_script_path]

    installer_command = [sys.executable, "-m", "nuitka"]
    installer_command += list(map(str, command))

    stime = time.time()
    LOGGER.info(f"starting nuitka with command={installer_command}")
    subprocess.run(installer_command, check=True, text=True)

    build_src_dir = workdir / (start_script_path.stem + ".dist")

    if overwrite_existing and target_dir.exists():
        LOGGER.debug(f"removing existing {target_dir}")
        shutil.rmtree(target_dir)

    LOGGER.info("copying build ...")
    shutil.copytree(build_src_dir, target_dir)

    LOGGER.info(f"build finished in {time.time() - stime}s")


def cli(argv=None):
    argv = argv or sys.argv[1:]
    workdir = THIS_DIR / ".workspace" / "nuitka"
    targetdir = THIS_DIR / ".workspace" / "build"

    parser = argparse.ArgumentParser(
        description="package knots-hub to a standalone executable",
    )
    parser.add_argument(
        "script_path",
        type=Path,
        help="filesystem path to a python file to use to start the application",
    )
    parser.add_argument(
        "--app_name",
        type=str,
        default=knots_hub.constants.EXECUTABLE_NAME,
        help="filename of the executable without the extension",
    )
    parser.add_argument(
        "--target_dir",
        type=Path,
        default=targetdir,
        help="filesystem path to a directory that may not exists",
    )
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="prevent disk overwrite if the build already exists",
    )
    parsed = parser.parse_args(argv)
    build(
        app_name=parsed.app_name,
        workdir=workdir,
        start_script_path=parsed.script_path,
        target_dir=parsed.target_dir,
        overwrite_existing=False if parsed.no_overwrite else True,
        icon_path=None,
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="{levelname: <7} | {asctime} [{name}] {message}",
        style="{",
        stream=sys.stdout,
    )
    cli()

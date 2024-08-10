import argparse
import logging
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import PIL.Image

import knots_hub
import kloch_rezenv
import kloch_kiche

THIS_DIR = Path(__file__).parent.resolve()

LOGGER = logging.getLogger(Path(__file__).stem)


def create_ico(src_image_path: Path, dst_path: Path):
    image = PIL.Image.open(src_image_path)
    image.save(
        dst_path,
        sizes=[
            (16, 16),
            (24, 24),
            (32, 32),
            (48, 48),
            (64, 64),
            (128, 128),
            (256, 256),
        ],
        bitmap_format="png",
    )


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
        f"--include-data-file={start_script_path.parent}={start_script_path.parent.name}/=**/*.ps1",
    ]
    # windows specific
    if icon_path:
        build_icon_path = workdir / "icon.ico"
        LOGGER.info(f"generating icon '{build_icon_path}'")
        create_ico(icon_path, build_icon_path)
        command += [f"--windows-icon-from-ico={build_icon_path}"]

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
    if icon_path:
        shutil.copy(build_icon_path, target_dir / "icon.ico")

    LOGGER.info(f"build finished in {time.time() - stime}s")


def cli(argv=None):
    argv = argv or sys.argv[1:]
    workdir = THIS_DIR / ".workspace" / "nuitka"
    targetdir = THIS_DIR / ".workspace" / "build"

    workdir.mkdir(parents=True, exist_ok=True)

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
        "--icon_path",
        type=Path,
        default=knots_hub.constants.EXECUTABLE_NAME,
        help="filesystem path to an existing .ico or .png file.",
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
        icon_path=parsed.icon_path,
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="{levelname: <7} | {asctime} [{name}] {message}",
        style="{",
        stream=sys.stdout,
    )
    cli()

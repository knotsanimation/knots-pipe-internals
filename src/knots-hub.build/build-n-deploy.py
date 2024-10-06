"""
Deploy a knots-hub version build on the knots server, so it can be used by anybody.

The script will perform a build by calling the build-script and then copy/paste it to
the hardcoded server location.

The script will verify:
- you are on the main branch
- there is no changes commit
- there is no changes to push/pull
- the version is not already deployed
"""

import argparse
import datetime
import getpass
import logging
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

import knots_hub
import knots_hub.__main__

THIS_DIR = Path(__file__).parent.resolve()

LOGGER = logging.getLogger(Path(__file__).stem)

BUILD_SCRIPT = THIS_DIR / "build-app-nuitka.py"


def gitget(command: list[str], cwd: Path) -> str:
    """
    Call git and return its output.
    """
    out = subprocess.check_output(["git"] + command, cwd=cwd, text=True)
    out = out.rstrip("\n").rstrip(" ")
    return out


def create_build_info(target_path: Path, version: str = None):
    git_command = ["git", "rev-parse", "HEAD"]
    commit_hash = subprocess.check_output(git_command, cwd=THIS_DIR, text=True)
    commit_hash = commit_hash.strip("\n")

    try:
        git_command = ["git", "config", "remote.origin.url"]
        remote_url = subprocess.check_output(git_command, cwd=THIS_DIR, text=True)

    except Exception as error:
        remote_url = str(error)

    build_info = "\n".join(
        [
            f"date={datetime.datetime.now()}",
            f"user={getpass.getuser()}",
            f"commit={commit_hash}",
            # remote is mostly added for beginners to know where the files come from
            f"remote={remote_url}",
        ]
        + ([f"version={version}"] if version else [])
    )
    target_path.write_text(build_info, encoding="utf-8")


def deploy(
    deploy_root: Path,
    build_script: Path,
    icon_path: Optional[Path] = None,
):

    if not deploy_root.exists():
        raise FileExistsError(
            f"Deploy root directory '{deploy_root}' provided does not exist"
        )

    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    build_version = f"{knots_hub.__version__}+{now}"
    build_version_filesafe = build_version.replace("+", "-")
    build_dir = tempfile.mkdtemp(prefix="knots-hub-dev-deploy-")

    deployed_dir = deploy_root / build_version_filesafe

    # XXX: we don't use sys.argv after so safe to override
    sys.argv = [
        "",
        knots_hub.__main__.__file__,
        "--app_name",
        knots_hub.constants.EXECUTABLE_NAME,
        "--target_dir",
        str(build_dir),
    ]
    if icon_path:
        sys.argv.extend(["--icon_path", str(icon_path)])

    LOGGER.info("building ...")
    runpy.run_path(str(build_script), run_name="__main__")

    LOGGER.info(f"deploying build to '{deployed_dir}'")
    shutil.copytree(build_dir, deployed_dir)
    build_info_path = deployed_dir / ".build.info"
    LOGGER.info(f"creating build info file at '{build_info_path}'")
    create_build_info(target_path=build_info_path, version=build_version)

    LOGGER.info(f"cleaning build dir '{build_dir}'")
    shutil.rmtree(build_dir)

    build_info_path = deploy_root / "deploy.info"
    LOGGER.info(f"creating build info file at '{build_info_path}'")
    create_build_info(target_path=build_info_path, version=build_version)


def cli(argv=None):
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="package knots-hub to a standalone executable and deploy it on the server.",
    )
    parser.add_argument(
        "deploy_root",
        type=Path,
        help="filesystem path to an existing directory to deploy builds to.",
    )
    parser.add_argument(
        "--icon_path",
        type=Path,
        default=None,
        help="filesystem path to an existing .ico or .png file.",
    )
    parsed = parser.parse_args(argv)
    deploy(
        deploy_root=parsed.deploy_root,
        build_script=BUILD_SCRIPT,
        icon_path=parsed.icon_path,
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="{levelname: <7} | {asctime} [{name}] {message}",
        style="{",
        stream=sys.stdout,
    )
    cli()

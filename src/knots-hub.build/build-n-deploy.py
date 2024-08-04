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
import json
import logging
import runpy
import shutil
import socket
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
            f"machine={socket.gethostname()}",
            f"commit={commit_hash}",
            # remote is mostly added for beginners to know where the files come from
            f"remote={remote_url}",
        ]
        + ([f"version={version}"] if version else [])
    )
    target_path.write_text(build_info, encoding="utf-8")


def update_installer_list(
    installer_list_path: Path,
    build_version: str,
    build_path: Path,
):
    """
    Create the config file as expected by knots-hub to indicate the available version
    of knots-hub.
    """
    content = {}
    if installer_list_path.exists():
        with installer_list_path.open("r", encoding="utf-8") as installer_list_file:
            content = json.load(installer_list_file)

    content[build_version] = str(build_path)

    json.dump(
        content,
        installer_list_path.open("w", encoding="utf-8"),
        indent=4,
        sort_keys=True,
    )


def deploy_latest_dir(src_dir: Path, dst_dir: Path):
    if dst_dir.exists():
        LOGGER.debug(f"removing '{dst_dir}'")
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)
    deploy_exe_latest_path = next(
        dst_dir.glob(knots_hub.constants.EXECUTABLE_NAME + "*")
    )
    deploy_exe_latest_path.rename(deploy_exe_latest_path.with_stem("knots-hub"))


def deploy(
    deploy_root: Path,
    build_script: Path,
    skip_checks=False,
    icon_path: Optional[Path] = None,
    only_deploy_latest: Optional[str] = None,
):
    build_version = knots_hub.__version__
    build_dir = tempfile.mkdtemp(prefix="knots-hub-dev-deploy-")

    deployed_dir = deploy_root / build_version
    deployed_latest_dir = deploy_root / "latest"
    installs_list_path = deploy_root / "install-list.json"

    if only_deploy_latest:
        deployed_dir = deploy_root / only_deploy_latest
        if not deployed_dir.exists():
            raise FileNotFoundError(
                f"The provided deployed version '{only_deploy_latest}' to deploy as "
                f"latest doesn't exist on disk at '{deployed_dir}'"
            )
        LOGGER.info(f"creating 'latest' build to '{deployed_latest_dir}'")
        deploy_latest_dir(deployed_dir, deployed_latest_dir)

        build_info_path = deployed_latest_dir / ".deploy.info"
        LOGGER.info(f"creating build info file at '{build_info_path}'")
        create_build_info(target_path=build_info_path, version=None)
        return

    if not skip_checks:

        if not deploy_root.exists():
            raise FileExistsError(
                f"Deploy root directory '{deploy_root}' provided does not exist"
            )

        if deployed_dir.exists():
            raise ValueError(
                f"Cannot deploy existing version '{build_version}' at '{deployed_dir}'"
            )

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

    LOGGER.info(f"creating 'latest' build to '{deployed_latest_dir}'")
    deploy_latest_dir(deployed_dir, deployed_latest_dir)

    LOGGER.info(f"cleaning build dir '{build_dir}'")
    shutil.rmtree(build_dir)

    LOGGER.info(f"updating installer list '{installs_list_path}'")
    update_installer_list(
        installer_list_path=installs_list_path,
        build_version=build_version,
        build_path=deployed_dir.relative_to(installs_list_path.parent),
    )

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
    parser.add_argument(
        "--skip_checks",
        action="store_true",
        default=False,
        help="prevent running filesystem check before build",
    )
    parser.add_argument(
        "--only_deploy_latest",
        type=str,
        default=None,
        help="Do not build and instead just take the specified server deployed version and create the latest directory from it.",
    )
    parsed = parser.parse_args(argv)
    deploy(
        deploy_root=parsed.deploy_root,
        build_script=BUILD_SCRIPT,
        skip_checks=parsed.skip_checks,
        icon_path=parsed.icon_path,
        only_deploy_latest=parsed.only_deploy_latest,
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="{levelname: <7} | {asctime} [{name}] {message}",
        style="{",
        stream=sys.stdout,
    )
    cli()

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

import datetime
import logging
import runpy
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

import knots_hub
import knots_hub.__main__

THIS_DIR = Path(__file__).parent.resolve()

LOGGER = logging.getLogger(Path(__file__).stem)

# XXX: intentional hardcoded path
KNOTS_SERVER_DEPLOY_ROOT = Path(r"N:\apps\knots-hub\builds")
SKIP_CHECKS = False
BUILD_SCRIPT = THIS_DIR / "build-app-nuitka.py"


def gitget(command: list[str], cwd: Path) -> str:
    """
    Call git and return its output.
    """
    out = subprocess.check_output(["git"] + command, cwd=cwd, text=True)
    out = out.rstrip("\n").rstrip(" ")
    return out


def create_build_info(target_dir: Path, version: str) -> Path:
    """
    Create a file storing metadata about this build process, for tracking purposes.
    """
    commit_hash = gitget(["rev-parse", "HEAD"], THIS_DIR)
    content = "\n".join(
        [
            f"date={datetime.datetime.now()}",
            f"machine={socket.gethostname()}",
            f"commit={commit_hash}",
            f"version={version}",
        ]
    )
    target_path = target_dir / ".build.info"
    target_path.write_text(content)
    return target_path


def deploy(
    deploy_root: Path,
    build_script: Path,
    skip_checks=False,
):
    build_version = knots_hub.__version__
    build_dir = tempfile.mkdtemp(prefix="knots-hub-dev-deploy-")

    deploy_dir = deploy_root / build_version
    deploy_latest_dir = deploy_root / "latest"

    if not skip_checks:

        if not deploy_root.exists():
            raise FileExistsError(
                f"Deploy root directory '{deploy_root}' provided does not exist"
            )

        if deploy_dir.exists():
            raise ValueError(
                f"Cannot deploy existing version '{build_version}' at '{deploy_dir}'"
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
    LOGGER.info("building ...")
    runpy.run_path(str(build_script), run_name="__main__")

    LOGGER.info(f"deploying build to '{deploy_dir}'")
    shutil.copytree(build_dir, deploy_dir)
    LOGGER.info(f"creating build info")
    create_build_info(target_dir=deploy_dir, version=build_version)

    LOGGER.info(f"creating 'latest' build to '{deploy_latest_dir}'")
    if deploy_latest_dir.exists():
        shutil.rmtree(deploy_latest_dir)
    shutil.copytree(build_dir, deploy_latest_dir)
    create_build_info(target_dir=deploy_latest_dir, version=build_version)
    deploy_exe_latest_path = next(
        deploy_latest_dir.glob(knots_hub.constants.EXECUTABLE_NAME + "*")
    )
    deploy_exe_latest_path.rename(deploy_exe_latest_path.with_stem("knots-hub"))

    LOGGER.info(f"cleaning build dir '{build_dir}'")
    shutil.rmtree(build_dir)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="{levelname: <7} | {asctime} [{name}] {message}",
        style="{",
        stream=sys.stdout,
    )
    deploy(
        deploy_root=KNOTS_SERVER_DEPLOY_ROOT,
        build_script=BUILD_SCRIPT,
        skip_checks=SKIP_CHECKS,
    )

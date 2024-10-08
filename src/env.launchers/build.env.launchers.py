import argparse
import logging
import re
import runpy
import sys
from pathlib import Path
from typing import Callable

THIS_DIR = Path(__file__).parent.resolve()

LOGGER = logging.getLogger(Path(__file__).stem)

ENV_SCRIPT = THIS_DIR / "base.env.py"


def build_batch_env(environment: dict[str, str]) -> str:
    def _resolve_path(var_path: str | list[str]) -> str:
        if isinstance(var_path, list):
            return ";".join([_resolve_path(subvar) for subvar in var_path])
        # the dot in "%~dp0." is because dp0 have a trailing slash
        #   https://stackoverflow.com/a/25853380/13806195
        new_path = var_path.replace("@SCRIPTDIR@", "%~dp0.")
        new_path = new_path.replace("/", "\\")
        return new_path

    content = "@echo off\n"
    for var_name, var_value in environment.items():
        content += f'set "{var_name}={_resolve_path(var_value)}"\n'

    return content


def build_powershell_env(environment: dict[str, str]) -> str:
    def _resolve_path(var_path: str | list[str]) -> str:
        if isinstance(var_path, list):
            return ";".join([_resolve_path(subvar) for subvar in var_path])
        new_path = var_path.replace("@SCRIPTDIR@", "$PSScriptRoot")
        new_path = re.sub(r"%(\w+)%", r"${env:\g<1>}", new_path)
        new_path = new_path.replace("/", "\\")
        return new_path

    content = ""
    for var_name, var_value in environment.items():
        content += f'$env:{var_name} = "{_resolve_path(var_value)}"\n'

    return content


def build_shell_env(environment: dict[str, str]) -> str:
    def _resolve_path(var_path: str | list[str]) -> str:
        if isinstance(var_path, list):
            return ":".join([_resolve_path(subvar) for subvar in var_path])
        new_path = var_path.replace("@SCRIPTDIR@", "$(dirname $0)")
        new_path = re.sub(r"%(\w+)%", r"${\g<1>}", new_path)
        return new_path

    content = ""
    for var_name, var_value in environment.items():
        content += f'export {var_name}="{_resolve_path(var_value)}"\n'

    return content


BUILDERS = {
    "batch": build_batch_env,
    "powershell": build_powershell_env,
    "shell": build_shell_env,
}


def cli(argv=None):
    argv = argv or sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="build environment launchers",
    )
    parser.add_argument(
        "builder_type",
        type=str,
        choices=list(BUILDERS.keys()),
        help="Target language for the launcher to build.",
    )
    parser.add_argument(
        "target_path",
        type=Path,
        help="Filesystem path to the launcher to create.",
    )
    parsed = parser.parse_args(argv)

    builder: Callable[[dict], str] = BUILDERS[parsed.builder_type]
    target_path: Path = parsed.target_path

    print("generating environment variables")
    env_vars = runpy.run_path(str(ENV_SCRIPT), run_name="build")
    environment: dict[str, str] = env_vars["ENVIRONMENT"]
    content = builder(environment)
    print(f"writing launcher '{target_path}'")
    target_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="{levelname: <7} | {asctime} [{name}] {message}",
        style="{",
        stream=sys.stdout,
    )
    cli()

"""
define the environment variable common to each operatin system.

rules:
- define all path name separators with posix standard '/'
- environment variable are referenced using widnows standard %VARNAME%
"""

from pathlib import PurePosixPath

rootdir = PurePosixPath("@SCRIPTDIR@")
bindir = rootdir / "bin"
knotshubdir = rootdir / ".." / ".." / "apps" / "knots-hub"
buildir = knotshubdir / "builds"
configdir = knotshubdir / "configs"

# those 2 next variables determine which version of knots-hub the artist need to use
last_build_exe_name = "knots_hub-v0.11.1.exe"
last_build_name = "0.11.1-20241008211113"

last_build_version = last_build_name.replace("-", "+")
last_build_path = buildir / last_build_name

ENVIRONMENT = {
    "KNOTSHUB_SERVER_EXE_PATH": str(last_build_path / last_build_exe_name),
    "KNOTSHUB_INSTALLER": f"{last_build_version}={last_build_path}",
    "KNOTSHUB_USER_INSTALL_PATH": "%LOCALAPPDATA%/knots-hub",
    "KNOTSHUB_VENDOR_INSTALLER_CONFIG_PATHS": str(
        configdir / "knots-hub.vendor-installers.json"
    ),
    "KNOTSHUB_VENDOR_INSTALL_ROOT": "%LOCALAPPDATA%/knots-hub.vendors",
    "KNOTSHUB_VENDOR_REZ_ROOT": "%KNOTSHUB_VENDOR_INSTALL_ROOT%/rez",
    "PATH": [
        f"%PATH%",
        f"{bindir}",
    ],
}

if __name__ == "__main__":
    import json

    print(json.dumps(ENVIRONMENT, indent=4))

"""
define the environment variable common to each operatin system.

rules:
- define all path name separators with posix standard '/'
- environment variable are referenced using widnows standard %VARNAME%
"""

from pathlib import PurePosixPath

scriptdir = PurePosixPath("@SCRIPTDIR@")
bindir = scriptdir / ".." / "bin"
profilesdir = scriptdir / ".." / "profiles"
knotshubdir = scriptdir / ".." / ".." / "apps" / "knots-hub"
buildir = knotshubdir / "builds"
configdir = knotshubdir / "configs"

# those 2 next variables determine which version of knots-hub the artist need to use
last_build_exe_name = "knots_hub-v0.12.1.exe"
last_build_name = "0.12.1-20241020150112"

last_build_version = last_build_name.replace("-", "+")
last_build_path = buildir / last_build_name

ENVIRONMENT = {
    # meta variable to increment everytime this file is modified; for debugging
    "__KNOTS_ENV_VERSION__": "1",
    # __________________________
    # // knots-hub configuration
    "KNOTSHUB_SERVER_EXE_PATH": str(last_build_path / last_build_exe_name),
    "KNOTSHUB_INSTALLER": f"{last_build_version}={last_build_path}",
    "KNOTSHUB_USER_INSTALL_PATH": "%LOCALAPPDATA%/knots-hub",
    "KNOTSHUB_VENDOR_INSTALLER_CONFIG_PATHS": str(
        configdir / "knots-hub.vendor-installers.json"
    ),
    "KNOTSHUB_VENDOR_INSTALL_ROOT": "%LOCALAPPDATA%/knots-hub.vendors",
    "KNOTSHUB_VENDOR_REZ_ROOT": "%KNOTSHUB_VENDOR_INSTALL_ROOT%/rez",
    # ________________________________
    # // used by knots-hub indirectly:
    "REZ_LOCAL_DATA_ROOT": "%HOME%/rez",
    # defined here because need to be created before rez launch
    "REZ_CACHE_PACKAGES_PATH": "%REZ_LOCAL_DATA_ROOT%/.cache",
    # ________________________________
    # // used for the general pipeline
    "KNOTS_LOCAL_DATA_ROOT": "%LOCALAPPDATA%/knots",
    "PATH": [
        f"%PATH%",
        f"{bindir}",
    ],
    # ________
    # // kloch
    "KLOCH_CONFIG_CLI_LOGGING_PATHS": "%KNOTS_LOCAL_DATA_ROOT%/kloch.log",
    "KLOCH_CONFIG_CLI_SESSION_PATH": "%KNOTS_LOCAL_DATA_ROOT%/kloch-sessions",
    "KLOCH_CONFIG_PROFILE_ROOTS": str(profilesdir),
}

if __name__ == "__main__":
    import json

    print(json.dumps(ENVIRONMENT, indent=4))

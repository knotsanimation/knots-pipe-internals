@echo off

:: supposdly N:\apps\knots-hub\launchers
set "rootdir=%~dp0"
set "bindir=%rootdir%bin"
set "buildir=%rootdir%..\builds"
set "configdir=%rootdir%..\configs"

:: XXX: update those 3 variables to update the knots-hub version used by artists
set "latestbuild=%buildir%\0.9.1-20241006210225"
set "KNOTSHUB_SERVER_EXE_PATH=%latestbuild%\knots_hub-v0.9.1.exe"
set "KNOTSHUB_INSTALLER=0.9.1+20241006210225=%latestbuild%"

set "KNOTSHUB_USER_INSTALL_PATH=%LOCALAPPDATA%\knots-hub"
set "KNOTSHUB_VENDOR_INSTALLER_CONFIG_PATHS=%configdir%\knots-hub.vendor-installers.json"
:: not actually read by knots-hub but referenced in the installer config
set "KNOTSHUB_VENDOR_INSTALL_ROOT=%LOCALAPPDATA%\knots-hub.vendors"
set "KNOTSHUB_VENDOR_REZ_ROOT=%KNOTSHUB_VENDOR_INSTALL_ROOT%\rez"

set "PATH=%PATH%;%bindir%"

:: clear variables
set "rootdir="
set "bindir="
set "buildir="
set "configdir="
set "latestbuild="
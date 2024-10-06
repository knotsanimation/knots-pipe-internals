@echo off

:: supposdly N:\apps\knots-hub\launchers
set "rootdir=%~dp0"
set "buildir=%rootdir%..\builds"
set "configdir=%rootdir%..\configs"

:: XXX: update those 3 variables to update the knots-hub version used by artists
set "latestbuild=%buildir%\0.8.0-20241006142747"
set "exepath=%latestbuild%\knots_hub-v0.8.0.exe"
set "KNOTSHUB_INSTALLER=0.8.0+20241006142747=%latestbuild%"

set "KNOTSHUB_USER_INSTALL_PATH=%LOCALAPPDATA%\knots-hub"
set "KNOTSHUB_VENDOR_INSTALLERS_CONFIG=%configdir%\knots-hub.vendor-installers.json"
:: not actually read by knots-hub but referenced in the installer config
set "KNOTSHUB_VENDOR_INSTALL_ROOT=%LOCALAPPDATA%\knots-hub.vendors"
set "KNOTSHUB_VENDOR_REZ_ROOT=%KNOTSHUB_VENDOR_INSTALL_ROOT%\rez"

echo %date% %time% ^| starting %exepath%
echo (Press any key to exit the prompt once finished)
start "" /B /WAIT "%exepath%" %*
echo %date% %time% ^| initial hub session exited

pause >nul
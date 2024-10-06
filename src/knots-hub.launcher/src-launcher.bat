@echo off

:: supposdly N:\apps\knots-hub\launchers
set "rootdir=%~dp0"
set "buildir=%rootdir%..\builds"
set "configdir=%rootdir%..\configs"

set "KNOTSHUB_USER_INSTALL_PATH=%LOCALAPPDATA%\knots-hub"
set "KNOTSHUB_INSTALLER_LIST=%buildir%\install-list.json"
set "KNOTSHUB_VENDOR_INSTALLERS_CONFIG=%configdir%\knots-hub.vendor-installers.json"
:: not actually read by knots-hub but referenced in the installer config
set "KNOTSHUB_VENDOR_INSTALL_ROOT=%LOCALAPPDATA%\knots-hub.vendors"
set "KNOTSHUB_VENDOR_REZ_ROOT=%KNOTSHUB_VENDOR_INSTALL_ROOT%\rez"

:: we assume the shortcut link is still defined as "knots-hub"
:: (managed by knots-hub repository)
set "exepath=%KNOTSHUB_USER_INSTALL_PATH%\knots-hub.lnk"
set "restart="
:: if the program was never installed yet the server build will install it and
:: restart to it.
:: force-local-restart ensure we always prefer usage the locally installed program
:: whose location is defined by knots-hub internally
if not exist %exepath% (
   set "exepath=%buildir%\latest\knots-hub.exe"
   set "restart=--force-local-restart"
)

echo %date% %time% ^| starting %exepath%
echo (Press any key to exit the prompt once finished)
start "" /B /WAIT "%exepath%" %restart% %*
echo %date% %time% ^| initial hub session exited

pause >nul
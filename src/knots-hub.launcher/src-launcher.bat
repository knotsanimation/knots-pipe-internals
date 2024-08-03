@echo off

:: usually N:\apps\knots-hub
set "rootdir=%~dp0"
set "exepath=%rootdir%latest\knots-hub.exe"

set "KNOTSHUB_USER_INSTALL_PATH=%LOCALAPPDATA%\knots-hub"
set "KNOTSHUB_INSTALLER_LIST=%rootdir%install-list.json"
set "KNOTSHUB_VENDOR_INSTALLERS_CONFIG=%rootdir%..\configs\knots-hub.vendor-installers.json"
set "KNOTSHUB_VENDOR_INSTALL_PATH=%LOCALAPPDATA%\knots-hub.vendors"

:: force-local-restart ensure we always prefer usage the locally installed program
:: whose location is defined by knots-hub internally
::
:: if the program was never installed yet the server build will install it and
:: restart to it.
echo %date% %time% ^| starting %exepath%
echo (Press any key to exit the prompt once finished)
start "" /B /WAIT "%exepath%" --force-local-restart %*
echo %date% %time% ^| server hub exited

pause >nul
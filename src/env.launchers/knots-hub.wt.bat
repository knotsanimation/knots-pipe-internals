:: for Windows Terminal command line argument see:
:: https://learn.microsoft.com/en-gb/windows/terminal/command-line-arguments
:: for powershell command line argument see:
:: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_exe
start "" "%LocalAppData%\Microsoft\WindowsApps\wt.exe" --window 0 new-tab --title knots-hub powershell -NoExit -File "%~dp0.\setup-env.ps1"
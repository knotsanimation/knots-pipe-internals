param (
    [string]$shortcut_type = "ps1"
)

$ErrorActionPreference = "Stop"

$desktop_path = [Environment]::GetFolderPath([Environment+SpecialFolder]::Desktop)
$shortcut_path = "${desktop_path}\knots-hub.lnk"
$icon_path = "${PSScriptRoot}\..\launchers\icon.ico" | Resolve-Path
$reference_path = "${PSScriptRoot}\..\launchers\knots-hub.${shortcut_type}.lnk" | Resolve-Path

if (Test-Path $shortcut_path) {
    Remove-Item $shortcut_path -Force
}

Write-Output "creating shortcut to '$reference_path'"

# https://superuser.com/a/836818
$wsobject = New-Object -ComObject WScript.Shell;
$shortcut = $wsobject.CreateShortcut($shortcut_path);
# https://learn.microsoft.com/en-us/previous-versions/3s9bx7at(v=vs.80)
$shortcut.IconLocation = "$icon_path";
# note: a lnk targeting another lnk will just inherit the target lnk path expression
$shortcut.TargetPath = "$reference_path";
$shortcut.Save()

Write-Output "shortcut created at '$shortcut_path'"
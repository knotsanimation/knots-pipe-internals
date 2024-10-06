# error handling policy
set -euo pipefail

# ensure cwd is this script dir
cd "$(dirname "$0")" || exit

pyscript=$PWD/build-n-deploy.py

python_exe_path=${BUILD_PYTHON_PATH:-""}

rm .workspace --force --recursive
mkdir .workspace
cd .workspace || exit

# we assume we want to build the latest commit on the remote main branch
git clone https://github.com/knotsanimation/knots-hub.git knots-hub

poetry init --name knots-hub-build --no-interaction --python ^3.10
if [ -n "$python_exe_path" ]; then
  echo using $python_exe_path
	poetry env use "$python_exe_path"
else
  echo using current implicit python interpreter
  poetry env info
fi

poetry add ./knots-hub/
poetry add nuitka==2.4.2
poetry add Pillow  # needed for icon generation
echo "running build script '$pyscript'"
poetry run python "$pyscript" "N:\apps\knots-hub\builds" --icon_path "$PWD/knots-hub/icon.png" $@

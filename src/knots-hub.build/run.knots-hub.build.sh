# error handling policy
set -euo pipefail

# ensure cwd is this script dir
cd "$(dirname "$0")" || exit

pyscript=$PWD/build-n-deploy.py

rm .workspace --force --recursive
mkdir .workspace
cd .workspace || exit

# we assume we want to build the latest commit on the remote main branch
git clone https://github.com/knotsanimation/knots-hub.git knots-hub

poetry init --name knots-hub-build --no-interaction --python ^3.10
poetry add ./knots-hub/
poetry add nuitka==2.4.2
echo "running build script '$pyscript'"
poetry run python "$pyscript" "N:\apps\knots-hub\builds"

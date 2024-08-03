# knots-hub.launcher

A script that allow any user of the pipeline to start knots-hub.

The script purpose is mostly to configure knots-hub before launching it.

## usage

- make sure there is no uncommited changes in this repository
- execute [`deploy.knots-hub.launcher.py`](deploy.knots-hub.launcher.py)
with any python-3.7+ interpreter.

## design

Be careful as the script rely on the filesystem structure generated
by [../knots-hub.build](../knots-hub.build).

The build will deploy the `.bat` script on the server and create a Windows
shortcut to it.
# rez.extensions

Deploying some custom rez extensions stored in https://github.com/knotsanimation/rez_extensions.git

# usage

- make sure there is no uncommited changes in this repository
- execute [`deploy.rez.extensions.py`](deploy.rez.extensions.py)
with any python-3.7+ interpreter.
- verify the content is properly deployed on the server

# design

This will copy some of the content of the `rez_extension` git repository
to `N:\apps\rez\extensions`.

The deploy process will make a temporary backup of the existing directory
that should be restored if any Exception.
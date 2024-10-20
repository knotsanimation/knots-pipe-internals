# kloch.profiles

These are the profile describing the environments used by the studio.

> Check kloch documentation https://knotsanimation.github.io/kloch/file-format.html
 
All profile are made for the latest version of kloch being used in production
(packaged in the active knots-hub version).

## usage

- make sure there is no uncommited changes in this repository
- execute [`deploy.kloch.profiles.py`](deploy.kloch.profiles.py)
  with any python-3.7+ interpreter.

## design

The build will deploy the profiles on the server at `N:\env\profiles`
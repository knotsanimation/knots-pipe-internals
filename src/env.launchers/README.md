# env.launchers

Create and deploy scripts to configure the environment to launch knots-hub and the pipeline.

## usage

- make sure there is no uncommited changes in this repository
- execute [`deploy.knots-hub.launcher.py`](deploy.knots-hub.launcher.py)
  with any python-3.7+ interpreter.

## design

- [base.env.py](base.env.py) is an OS-agnostic way of specifying environment
  variables.
- [build.env.launchers.py](build.env.launchers.py) will call `base.env` and 
  generates a script on each os default language
- [deploy.env.launchers.py](deploy.env.launchers.py) calls the build script
  and copy files over to the server.

## development

- the icon is just copied from the latest knots-hub build on the server
- some of the paths in [base.env.py](base.env.py) depends on the structure
  generated by `knots-hub.build`.
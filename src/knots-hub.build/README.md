# knots-hub.build

Build system to create a standalone executable for knots-hub and deploy it on
the server.

The build system use [nuitka](https://nuitka.net/) for packaging.

Each build is timestamped to the current date so running the script 2 time will
produce 2 build on the server.

Builds use the latest version of knots-hub available remotely by default.

Once a build is completed and tested you can make it availble to user by updating
the launchers.

# usage

- you might need to set the `BUILD_PYTHON_PATH` env var to set the path
  to the python interpreter to use for the venv.
- execute [`run.knots-hub.build.sh`](run.knots-hub.build.sh), everything else
  is automatic.

> [!TIP]
> Call `run.knots-hub.build.sh --help` to see build options


## server output

Write files in root directory `N:\apps\knots-hub\builds`:

- a directory for the currently built version
- `deploy.info` metadata file


## troubleshooting

### issue with last build

If you have any problem with the last build you just deploy on the server,
you could delete it version folder on the server and restart the build.




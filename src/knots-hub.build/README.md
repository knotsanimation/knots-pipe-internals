# knots-hub.build

Build system to create a standalone executable for knots-hub and deploy it on
the server.

The build system use [nuitka](https://nuitka.net/) for packaging.

We assume you ALWAYS want to build a newer version relative to existing
deployed version.

# usage

- you might need to set the `BUILD_PYTHON_PATH` env var to set the path
  to the python interpreter to use for the venv.
- execute [`run.knots-hub.build.sh`](run.knots-hub.build.sh), everything else
  is automatic.

Be careful when building a new knots-hub version with breaking change affecting
the configs, you will also need to update and deploy those **at the same time**.

## server output

Write files in root directory `N:\apps\knots-hub\builds`:

- a directory for the currently built version
- a `latest` directory, copy of the first directory
- append/create the `install-list.json` used by the hub at runtime

## troubleshooting

### issue with last build

If you have any problem with the last build you just deploy on the server,
you could delete it version folder on the server and restart the build.

However keep in mind that if someone started knots-hub in the interval since 
the build is deployed on the server then this might create issues for
this user.



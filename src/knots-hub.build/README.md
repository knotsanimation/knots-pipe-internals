# knots-hub.build

Build system to create a standalone executable for knots-hub and deploy it on
the server.

The build system use [nuitka](https://nuitka.net/) for packaging.

We assume you ALWAYS want to build a newer version relative to existing
deployed version.

# usage

execute [`run.knots-hub.build.sh`](run.knots-hub.build.sh), everything else is automatic.

## server output

Write files in root directory `N:\apps\knots-hub\builds`:

- a directory for the currently built version
- a `latest` directory, copy of the first directory




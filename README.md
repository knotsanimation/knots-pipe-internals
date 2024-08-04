# knots-pipe-internals

This repository act as the manager layer between remote code and the server, i.e.
we store deploy script for some our software here.

As such this repository is aware of, and define the server file structure.

To avoid creating too many repositories we also store software configs there.

## pre-requisites

The deploy script may need some of the following software:

- a _python_ interpreter (3.7+)
- _git-bash_ to execute shell script on Windows
- _git_ installed and available via the `git` command

If you want to install some depencies for developing code, `poetry` will be 
required to interpret the `pyproject.toml` (the dependencies are not
required for deploying).

## usage

Each "deployment recipe" in [src/](src) is independant of each other (but can
have an implicit dependency on another). The README in each directory should give
you more detailed usage instructions.

## issues

Sometimes you can get weird error when deploying on the server. If that happens
check the error first and if you don't understand try to rerun the deploy script.
Make sure eveything is deployed properly afterwhile.
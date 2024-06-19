# ska-tmc-cdm
The repository for the SKA Control Data Model.

## Project description

This project contains the code for the SKA Control Data Model, which provides
Python/JSON serialisation for the command arguments for various TMC interfaces
with other subsystems.

This library can marshal JSON for the following Tango devices.

- TMC CentralNode
- TMC SubArrayNode
- MCCSController
- MCCSSubarray

## Quickstart

This project is structured to use Docker containers for development and
testing so that the build environment, test environment and test results are
all completely reproducible and are independent of host environment. It uses
``make`` to provide a consistent UI.

First, clone this repository with:

```
git clone --recurse-submodules git@gitlab.com:ska-telescope/ska-tmc-cdm.git
```

To refresh the GitLab Submodule, execute below commands:

```
git submodule update --recursive --remote
git submodule update --init --recursive
```


Install all dependencies using Poetry:
First go to the poetry shell, It opens the poetry virtual environment and then run poetry install command

```
> poetry shell

> poetry install
```

To update the poetry.lock file, use command:

```
> poetry update
```

Build a new Docker image for the CDM,run:

```
make oci-build
```

Execute the unit tests and lint the project with:

```
make python-test && make python-lint
```


Format the Python code:

```
make python-format
```

## Testing

You can execute unit tests with

```
make python-test
```

**Note:** These unit tests rely on a local copy of the telescope model data downloaded
to `tests/fixtures/tmdata/`. Updating the `ska-telmodel` library should automatically
refresh this downloaded data on your workstation, but in some cases you may need to run:

```shell
rm -r tests/fixtures/tmdata/
make tests/fixtures/tmdata/
```

to delete the old data and download a fresh copy of the new version.


## Release a new version

See SKAO instructions [here](https://developer.skao.int/en/latest/tools/software-package-release-procedure.html#software-package-release-procedure)


## Documentation


[![Documentation Status](https://readthedocs.org/projects/ska-telescope-ska-tmc-cdm/badge/?version=latest)](https://developer.skao.int/projects/ska-tmc-cdm/en/latest/?badge=latest)

Documentation can be found in the ``docs`` folder. To build docs, install the
documentation specific requirements:

```
pip3 install sphinx sphinx-rtd-theme recommonmark
```

and build the documentation (will be built in docs/build folder) with

```
make docs-build html
```


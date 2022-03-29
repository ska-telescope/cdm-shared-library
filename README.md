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

To clone this repository, run

```
git clone --recurse-submodules git@gitlab.com:ska-telescope/ska-tmc-cdm.git
```

To refresh the GitLab Submodule, execute below commands:

```
git submodule update --recursive --remote
git submodule update --init --recursive
```

## Build and test

Execute the test suite and lint the project with:

```
make python-test
make python-lint
```

To build a new Docker image, run

```
make oci-build
```

To rebuild the PlantUML diagrams after modification, from a
non-interactive session run

```
make diagrams
```

[![Documentation Status](https://readthedocs.org/projects/ska-telescope-ska-tmc-cdm/badge/?version=latest)](https://developer.skao.int/projects/ska-tmc-cdm/en/latest/?badge=latest)

Documentation can be found in the ``docs`` folder.


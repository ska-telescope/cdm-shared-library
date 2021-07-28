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

Build a new Docker image for the OET with:

```
make build
```

Execute the test suite with:
```
make test
```

Launch an interactive shell inside a container, with your workspace visible
inside the container:

```
make interactive
```

[![Documentation Status](https://readthedocs.org/projects/ska-telescope-ska-tmc-cdm/badge/?version=latest)](https://developer.skao.int/projects/ska-tmc-cdm/en/latest/?badge=latest)

Documentation can be found in the ``docs`` folder.


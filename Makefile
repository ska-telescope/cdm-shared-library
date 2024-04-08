#
# CAR_OCI_REGISTRY_USER  and PROJECT are combined to define the Docker
# tag for this project. The definition below inherits the standard
# value for CAR_OCI_REGISTRY_USER  (=artefact.skao.int) and overwrites
# PROJECT to give a final Docker tag of artefact.skao.int/ska-tmc-cdm
#
CAR_OCI_REGISTRY_HOST ?= artefact.skao.int
CAR_OCI_REGISTRY_USERNAME ?= ska-telescope
PROJECT_NAME := ska-tmc-cdm
TMDATA_VERSION := $(shell python -c 'from importlib.metadata import version; print(version("ska_telmodel"))')

OCI_IMAGE_BUILD_CONTEXT = $(PWD)
# unset defaults so settings in pyproject.toml take effect
PYTHON_SWITCHES_FOR_BLACK =
PYTHON_SWITCHES_FOR_ISORT =

# disable convention and refactoring lint warnings
PYTHON_SWITCHES_FOR_PYLINT = --disable=C,R

# resolve various conflicts with Black formatting
PYTHON_SWITCHES_FOR_FLAKE8 = --max-line-length=88 \
							 --exclude=tests/fixtures/ \
							 --extend-ignore=E501,W291,W503 \
							 --ignore

# include makefile to pick up the standard Make targets from the submodule
-include .make/base.mk
-include .make/python.mk
-include .make/oci.mk

# include your own private variables for custom deployment configuration
-include PrivateRules.mak
python-pre-test: tests/fixtures/tmdata/

tests/fixtures/tmdata/:
	ska-telmodel cp -UR --sources=car://gitlab.com/ska-telescope/ska-telmodel?${TMDATA_VERSION}#tmdata "" tests/fixtures/tmdata

diagrams:  ## recreate PlantUML diagrams whose source has been modified
	@for i in $$(git diff --name-only -- '*.puml'); \
	do \
		echo "Recreating $${i%%.*}.png"; \
		cat $$i | docker run --rm -i think/plantuml -tpng $$i > $${i%%.*}.png; \
	done

#
# CAR_OCI_REGISTRY_HOST, CAR_OCI_REGISTRY_USERNAME and PROJECT_NAME are combined to define
# the Docker tag for this project. The definition below inherits the standard
# value for CAR_OCI_REGISTRY_HOST (=artefact.skao.int) and overwrites
# PROJECT to give a final Docker tag of artefact.skao.int/ska-tmc-cdm
#
CAR_OCI_REGISTRY_HOST ?= artefact.skao.int
CAR_OCI_REGISTRY_USERNAME ?= ska-telescope
PROJECT_NAME = ska-tmc-cdm

OCI_IMAGE_BUILD_CONTEXT = $(PWD)

# include makefile to pick up the standard Make targets from the submodule
-include .make/base.mk
-include .make/python.mk
-include .make/oci.mk

# include your own private variables for custom deployment configuration
-include PrivateRules.mak

diagrams:  ## recreate PlantUML diagrams whose source has been modified
	@for i in $$(git diff --name-only -- '*.puml'); \
	do \
		echo "Recreating $${i%%.*}.png"; \
		cat $$i | docker run --rm -i think/plantuml -tpng $$i > $${i%%.*}.png; \
	done

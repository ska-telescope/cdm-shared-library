#
# Project makefile for a Tango project. You should normally only need to modify
# CAR_OCI_REGISTRY_USER and PROJECT below.
#

#
# CAR_OCI_REGISTRY_USER  and PROJECT are combined to define the Docker
# tag for this project. The definition below inherits the standard
# value for CAR_OCI_REGISTRY_USER  (=artefact.skao.int) and overwrites
# PROJECT to give a final Docker tag of artefact.skao.int/ska-tmc-cdm
#
CAR_OCI_REGISTRY_HOST ?= artefact.skao.int
CAR_OCI_REGISTRY_USERNAME ?= ska-telescope
PROJECT = ska-tmc-cdm

# Docker, K8s and Gitlab CI variables
# gitlab-runner debug mode - turn on with non-empty value
RDEBUG ?=
# gitlab-runner executor - shell or docker
EXECUTOR ?= shell
# DOCKER_HOST connector to gitlab-runner - local domain socket for shell exec
DOCKER_HOST ?= unix:///var/run/docker.sock
# DOCKER_VOLUMES pass in local domain socket for DOCKER_HOST
DOCKER_VOLUMES ?= /var/run/docker.sock:/var/run/docker.sock
# registry credentials - user/pass/registry - set these in PrivateRules.mak
CAR_OCI_REGISTRY_USER_LOGIN ?=  ## registry credentials - user - set in PrivateRules.mak
CI_REGISTRY_PASS_LOGIN ?=  ## registry credentials - pass - set in PrivateRules.mak
CI_REGISTRY ?= gitlab.com/ska-telescope/ska-tmc-cdm

CI_PROJECT_DIR ?= .

CAR_PYPI_REPOSITORY_URL ?= https://artefact.skao.int/repository/pypi-internal/simple

# define private overrides for above variables in here
-include PrivateRules.mak

#
# include makefile to pick up the standard Make targets, e.g., 'make build'
# build, 'make push' docker push procedure, etc. The other Make targets
# ('make interactive', 'make test', etc.) are defined in this file.
#
include .make/docker.mk
include .make/release.mk

post-push:
	@. $(RELEASE_SUPPORT) ; differsFromRelease || docker push $(IMAGE):$(VERSION) ;

help:  ## show this help.
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

diagrams:  ## recreate PlantUML diagrams whose source has been modified
	@for i in $$(git diff --name-only -- '*.puml'); \
	do \
		echo "Recreating $${i%%.*}.png"; \
		cat $$i | docker run --rm -i think/plantuml -tpng $$i > $${i%%.*}.png; \
	done

.PHONY: all post-push help

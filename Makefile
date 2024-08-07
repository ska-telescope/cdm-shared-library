.PHONY: tests/fixtures/tmdata/ diagrams

PROJECT_NAME := ska-tmc-cdm
TMDATA_VERSION := $(shell python -c 'from importlib.metadata import version; print(version("ska_ost_osd"))')

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

# include your own private variables for custom deployment configuration
-include PrivateRules.mak
python-pre-test: tests/fixtures/tmdata/

# Static type-checking
# https://microsoft.github.io/pyright/
python-post-lint:
	pyright src/

tests/fixtures/tmdata/:
ifneq ($(TMDATA_VERSION), $(shell cat tests/fixtures/tmdata/TMDATA_VERSION))
	rm -rf tests/fixtures/tmdata
	ska-telmodel -U --sources=car:ost/ska-ost-osd?${TMDATA_VERSION} cp -R "" tests/fixtures/tmdata
	echo ${TMDATA_VERSION} > tests/fixtures/tmdata/TMDATA_VERSION
else
	$(info tests/fixtures/tmdata already current v${TMDATA_VERSION})
endif


diagrams:  ## recreate PlantUML diagrams whose source has been modified
	@for i in $$(git diff --name-only -- '*.puml'); \
	do \
		echo "Recreating $${i%%.*}.png"; \
		cat $$i | docker run --rm -i think/plantuml -tpng $$i > $${i%%.*}.png; \
	done

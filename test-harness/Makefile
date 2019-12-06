# Use bash shell with pipefail option enabled so that the return status of a
# piped command is the value of the last (rightmost) commnand to exit with a
# non-zero status. This lets us pipe output into tee but still exit on test
# failures.
SHELL = /bin/bash
.SHELLFLAGS = -o pipefail -c

all: test

# wait for the device to be available before beginning the test
# A temporary volume is mounted at /build when 'make test' is executing.
# The following steps copy across useful output to this volume which can
# then be extracted to form the CI summary for the test procedure.
test:
	cd /app && python setup.py test | tee setup_py_test.stdout
	-cd /app && ./code-analysis.sh | tee code_analysis.stdout
	if [ -d /build ]; then \
		mv /app/setup_py_test.stdout /build; \
		mv /app/code_analysis.stdout /build; \
		mv /app/htmlcov /build; \
		mv /app/coverage.xml /build; \
	fi;

# wait for the device to be available before beginning the test
# A temporary volume is mounted at /build when 'make test' is executing.
# The following steps copy across useful output to this volume which can
# then be extracted to form the CI summary for the test procedure.
# FIXME: Add pylint2junit to the tango-builder:latest image so that we don't need to install it here.
# FIXME: Missing functionality in pylint2junit prevents converting from parseable to xml. Once it's implemented there is no need to run linting twice.
lint:
	pip3 install pylint2junit; \
	mkdir -p /build/reports; \
	cd /app && pylint --exit-zero --output-format=parseable ska tests| tee /build/code_analysis.stdout; \
	cd /app && pylint --exit-zero --output-format=pylint2junit.JunitReporter ska tests | tee /build/reports/linting.xml;
	exit 0;

.PHONY: all test lint

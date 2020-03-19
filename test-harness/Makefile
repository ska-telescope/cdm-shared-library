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
test: lint
	cd /app && python3 setup.py test | tee setup_py_test.stdout
	if [ -d /build ]; then \
		mv /app/setup_py_test.stdout /build; \
		mv /app/htmlcov /build; \
		mv /app/coverage.xml /build; \
	fi;

lint:
	if [ -d /build ]; then \
		cd /app && pylint --output-format=parseable src/ska | tee /build/code_analysis.stdout; \
		cd /app && pylint --output-format=parseable tests/ska | tee -a /build/code_analysis.stdout; \
	fi;

.PHONY: all test lint

ARG BUILD_IMAGE="artefact.skao.int/ska-tango-images-pytango-builder:9.4.1"
ARG BASE_IMAGE="artefact.skao.int/ska-tango-images-pytango-runtime:9.4.1"
ARG CAR_OCI_REGISTRY_HOST=artefact.skao.int

# ignore DL3006: tag the version of an image explicitly
# hadolint ignore=DL3006
FROM $BUILD_IMAGE AS buildenv
# hadolint ignore=DL3006
FROM $BASE_IMAGE

ARG CAR_PYPI_REPOSITORY_URL=https://artefact.skao.int/repository/pypi-internal
ENV PIP_INDEX_URL=${CAR_PYPI_REPOSITORY_URL}

USER root

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* ./

# Install runtime dependencies and the app
RUN poetry export --format requirements.txt --output poetry-requirements.txt --without-hashes && \
    pip install -r poetry-requirements.txt && \
    rm poetry-requirements.txt && \
    pip install . \
    pip install ska_telmodel-1.9.1-py3-none-any.whl --force-reinstall

USER tango

CMD ["python3"]

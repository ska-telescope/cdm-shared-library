ARG BUILD_IMAGE="artefact.skao.int/ska-tango-images-pytango-builder:9.3.28"
ARG BASE_IMAGE="artefact.skao.int/ska-tango-images-pytango-runtime:9.3.16"
ARG CAR_OCI_REGISTRY_HOST=artefact.skao.int

# ignore DL3006: tag the version of an image explicitly
# hadolint ignore=DL3006
FROM $BUILD_IMAGE AS buildenv
# hadolint ignore=DL3006
FROM $BASE_IMAGE

ARG CAR_PYPI_REPOSITORY_URL=https://artefact.skao.int/repository/pypi-internal
ENV PIP_INDEX_URL=${CAR_PYPI_REPOSITORY_URL}

# Install Poetry
USER root
WORKDIR /app
COPY pyproject.toml poetry.lock* ./

# Install runtime dependencies and the app
RUN poetry install --no-dev

USER tango
RUN poetry config virtualenvs.create false

CMD ["python3"]

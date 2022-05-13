ARG CAR_OCI_REGISTRY_HOST=artefact.skao.int

FROM $CAR_OCI_REGISTRY_HOST/ska-tango-images-pytango-builder:9.3.14 AS buildenv
FROM $CAR_OCI_REGISTRY_HOST/ska-tango-images-pytango-runtime:9.3.14 AS runtime

ARG CAR_PYPI_REPOSITORY_URL=https://artefact.skao.int/repository/pypi-internal
ENV PIP_INDEX_URL ${CAR_PYPI_REPOSITORY_URL}/simple

ENV PATH "/home/tango/.local/bin:${PATH}"

# Install Poetry
USER root
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python - && \
    cd /usr/local/bin && \
    chmod a+x /opt/poetry/bin/poetry && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo \
COPY pyproject.toml poetry.lock* ./

# Install runtime dependencies and the app
RUN poetry install #--no-dev

CMD ["python3"]

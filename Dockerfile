ARG CAR_OCI_REGISTRY_HOST

FROM $CAR_OCI_REGISTRY_HOST/ska-tango-images-pytango-builder:9.3.10 AS buildenv
FROM $CAR_OCI_REGISTRY_HOST/ska-tango-images-pytango-runtime:9.3.10 AS runtime

ARG CAR_PYPI_REPOSITORY_URL
ENV PIP_INDEX_URL ${CAR_PYPI_REPOSITORY_URL}/simple

ENV PATH "/home/tango/.local/bin:${PATH}"

## Developers sometimes need to develop against unreleased code. To do so,
## we need to install code directly from GitLab - probably a feature branch -
## rather than pulling wheels from the SKA artefact repository. The steps
## below show how to do that for the Telescope Model dependency used by this
## project. First it installs git, then installs an SKA project directly from
## GitLab.
##
## install git
#USER root
##RUN --mount=type=cache,target=/var/lib/apt \
#RUN \
#    runtimeDeps='git' \
#    && DEBIAN_FRONTEND=noninteractive apt-get update \
#    && apt-get -y install --no-install-recommends $runtimeDeps
#USER tango
#
## install telescope model from an existing branch
## Exchange the RUN statements to cache pip wheels. Useful for developer environments.
##RUN --mount=type=cache,target=/home/tango/.cache/pip,uid=1000,gid=1000 \
#RUN \
#    python3 -m pip install \
#    --use-feature=in-tree-build \
#    git+https://gitlab.com/ska-telescope/telescope-model@at2-xxx-branch-name

## Exchange the RUN statements to cache pip wheels. Useful for developer environments.
#RUN --mount=type=cache,target=/home/tango/.cache/pip,uid=1000,gid=1000 \
RUN \
    python3 -m pip install \
    --use-feature=in-tree-build \
    # Running tests via an IDE required the test dependencies to be installed.
    # The quickest way to achieve this is by uncommenting the line below
#     -r tests/requirements.txt \
    .

CMD ["python3"]

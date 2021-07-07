FROM artefact.skao.int/ska-tango-images-pytango-builder:9.3.10 AS buildenv
FROM artefact.skao.int/ska-tango-images-pytango-runtime:9.3.10 AS runtime

ENV PATH="/home/tango/.local/bin:${PATH}"

# Developers sometimes need to develop against unreleased code. To do so,
# we need to install code directly from GitLab - probably a feature branch -
# rather than pulling wheels from the SKA artefact repository. The steps
# below show how to do that for the Telescope Model dependency used by this
# project. First it installs git, then installs an SKA project directly from
# GitLab.
#
## install git
USER root
RUN runtimeDeps='git' \
    && DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get -y install --no-install-recommends $runtimeDeps \
    && rm -rf /var/lib/apt/lists/* /etc/apt/apt.conf.d/30proxy
USER tango
#
# install telescope model from AT2-698 branch
# Exchange the RUN statements to cache pip wheels. Useful for developer environments.
#RUN --mount=type=cache,target=/home/tango/.cache/pip,uid=1000,gid=1000 \
RUN \
    python3 -m pip install \
    --extra-index-url https://nexus.engageska-portugal.pt/repository/pypi/simple \
    git+https://gitlab.com/ska-telescope/telescope-model@at1-905

# Exchange the RUN statements to cache pip wheels. Useful for developer environments.
#RUN --mount=type=cache,target=/home/tango/.cache/pip,uid=1000,gid=1000 \
RUN \
    python3 -m pip install \
    --extra-index-url https://nexus.engageska-portugal.pt/repository/pypi/simple \
    #--extra-index-url https://artefact.skao.int/repository/pypi/simple \
    # Running tests via an IDE required the test dependencies to be installed.
    # The quickest way to achieve this is by uncommenting the line below
     -r tests/requirements.txt \
    .

CMD ["python3"]

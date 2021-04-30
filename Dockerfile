FROM nexus.engageska-portugal.pt/ska-docker/ska-python-buildenv:9.3.3.1 AS buildenv
FROM nexus.engageska-portugal.pt/ska-docker/ska-python-runtime:9.3.3.1 AS runtime

ENV PATH="/home/tango/.local/bin:${PATH}"

# install git
USER root
RUN runtimeDeps='git' \
    && DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get -y install --no-install-recommends $runtimeDeps \
    && rm -rf /var/lib/apt/lists/* /etc/apt/apt.conf.d/30proxy
USER tango

# install telescope model from AT2-698 branch
# Exchange the RUN statements to cache pip wheels. Useful for developer environments.
#RUN --mount=type=cache,target=/home/tango/.cache/pip,uid=1000,gid=1000 \
RUN \
    python3 -m pip install \
    --extra-index-url https://nexus.engageska-portugal.pt/repository/pypi/simple \
    git+https://gitlab.com/ska-telescope/telescope-model@at2-698-add-tmc-to-telescope-model


# Exchange the RUN statements to cache pip wheels. Useful for developer environments.
#RUN --mount=type=cache,target=/home/tango/.cache/pip,uid=1000,gid=1000 \
RUN \
    python3 -m pip install \
    --extra-index-url https://nexus.engageska-portugal.pt/repository/pypi/simple \
    # Running tests via an IDE required the test dependencies to be installed.
    # The quickest way to achieve this is by uncommenting the line below
    # -r tests/requirements.txt \
    .

CMD ["python3"]

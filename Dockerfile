FROM nexus.engageska-portugal.pt/ska-docker/ska-python-buildenv:9.3.1 AS buildenv
FROM nexus.engageska-portugal.pt/ska-docker/ska-python-runtime:9.3.1 AS runtime

RUN python3 -m pip install -e . --extra-index-url https://nexus.engageska-portugal.pt/repository/pypi/simple

CMD ["python3"]

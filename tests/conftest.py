from pathlib import Path

import pytest

pytest_plugins = [
    "tests.fixtures.builder_pattern.assign_resource",
    "tests.fixtures.builder_pattern.configure_resource",
]


HERE = Path(__file__).parent.resolve()


@pytest.fixture(autouse=True)
def local_tmdata(monkeypatch):
    fixture_tmdata = str(HERE / "fixtures/tmdata")
    monkeypatch.setenv("SKA_TELMODEL_SOURCES", fixture_tmdata)

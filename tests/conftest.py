from pathlib import Path

import pytest

HERE = Path(__file__).parent.resolve()


@pytest.fixture(autouse=True)
def local_tmdata(monkeypatch):
    fixture_tmdata = str(HERE / "unit/fixture_data/ska-telmodel/tmdata")
    monkeypatch.setenv("SKA_TELMODEL_SOURCES", fixture_tmdata)

from pathlib import Path

import pytest

HERE = Path(__file__).parent.resolve()


@pytest.fixture(autouse=True)
def local_tmdata(monkeypatch):
    fixture_tmdata = str(HERE / "fixtures/tmdata")
    monkeypatch.setenv("SKA_TELMODEL_SOURCES", fixture_tmdata)


@pytest.fixture(autouse=True)
def allow_strict_telmodel_validation(monkeypatch):
    """
    Allow strictness=2 for CDM unit tests.

    ska-telmodel v1.20 changed behaviour so that strictness=2 is downgraded to
    strictness=1 unless certain recognised environment variables are set. This
    fixture sets one of those environment variables.
    """
    monkeypatch.setenv("SKA_TELMODEL_ALLOW_STRICT_VALIDATION", "1")

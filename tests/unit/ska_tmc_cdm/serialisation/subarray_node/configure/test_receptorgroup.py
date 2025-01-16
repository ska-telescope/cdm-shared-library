from functools import partial

import pytest

from ska_tmc_cdm import CODEC
from ska_tmc_cdm.messages.subarray_node.configure.receptorgroup import (
    FixedTrajectory,
    Projection,
    ProjectionAlignment,
    ProjectionType,
    ReceptorGroup,
    TableTrajectory,
)
from tests.utils import assert_json_is_equal

from ...test_skydirection import TestICRSField


class TestFixedTrajectory:
    FULL_JSON = """
    {
        "name": "fixed",
        "attrs": {
            "x": 12.34,
            "y": 56.78
        }
    }
    """

    full_instance = partial(
        FixedTrajectory, attrs=FixedTrajectory.Attrs(x=12.34, y=56.78)
    )

    def test_round_trip(self):
        """
        Test serialisation and deserialisation of a fully-defined
        FixedTrajectory.
        """
        instance = TestFixedTrajectory.full_instance()
        assert_json_is_equal(
            TestFixedTrajectory.FULL_JSON, CODEC.dumps(instance)
        )
        assert instance == CODEC.loads(
            FixedTrajectory, TestFixedTrajectory.FULL_JSON
        )


class TestTableTrajectory:
    FULL_JSON = """
    {
        "name": "table",
        "attrs": {
            "x": [1.1, 2.2, 3.3],
            "y": [4.4, 5.5, 6.6],
            "t": [7.7, 8.8, 9.9]
        }
    }
    """

    full_instance = partial(
        TableTrajectory,
        attrs=TableTrajectory.Attrs(
            x=[1.1, 2.2, 3.3], y=[4.4, 5.5, 6.6], t=[7.7, 8.8, 9.9]
        ),
    )

    def test_round_trip(self):
        """
        Test serialisation and deserialisation of a fully-defined
        TableTrajectory.
        """
        instance = TestTableTrajectory.full_instance()
        assert_json_is_equal(
            TestTableTrajectory.FULL_JSON, CODEC.dumps(instance)
        )
        assert instance == CODEC.loads(
            TableTrajectory, TestTableTrajectory.FULL_JSON
        )


class TestProjection:
    FULL_JSON = """
    {
        "name": "SSN",
        "alignment": "ICRS"
    }
    """

    full_instance = partial(
        Projection, name=ProjectionType.SSN, alignment=ProjectionAlignment.ICRS
    )

    def test_round_trip(self):
        instance = TestProjection.full_instance()
        assert_json_is_equal(TestProjection.FULL_JSON, CODEC.dumps(instance))
        assert instance == CODEC.loads(Projection, TestProjection.FULL_JSON)

    def test_partial_instance_round_trip(self):
        """
        Round trip to confirm successful serialisation and deserialisation of
        the smallest possible Projection where none of the optional attributes
        are defined.
        """
        instance = Projection()
        # empty JSON so should get the defaults
        assert instance == CODEC.loads(Projection, "{}")
        # ... but those defaults should be written out when serialised
        # TBC is this the right thing to do? When attributes take the default
        # should they be exported as None, export the (current) default value
        # the attribute assumed, or omitted from the JSON?
        assert_json_is_equal(TestProjection.FULL_JSON, CODEC.dumps(instance))


class TestReceptorGroup:
    FULL_JSON = (
        """
    {
        "receptors": ["SKA001", "SKA036", "SKA063", "SKA100"],
        "field": """
        + TestICRSField.FULL_JSON
        + """,
        "trajectory": """
        + TestFixedTrajectory.FULL_JSON
        + """,
        "projection": """
        + TestProjection.FULL_JSON
        + """
    }
    """
    )

    # structure expected from scan 2 onwards in a mosaic. Field could also be
    # defined, or projection omitted, but it'd be unusual. The main point is
    # that field and receptors are omitted but this should still be valid.
    MOSAIC_DELTA_JSON = (
        """
    {
        "trajectory": """
        + TestFixedTrajectory.FULL_JSON
        + """,
        "projection": """
        + TestProjection.FULL_JSON
        + """
    }
    """
    )

    full_instance = partial(
        ReceptorGroup,
        receptors={"SKA001", "SKA036", "SKA063", "SKA100"},
        field=TestICRSField.FULL_INSTANCE,
        trajectory=TestFixedTrajectory.full_instance(),
        projection=TestProjection.full_instance(),
    )

    mosaic_delta_instance = partial(
        ReceptorGroup,
        trajectory=TestFixedTrajectory.full_instance(),
        projection=TestProjection.full_instance(),
    )

    @pytest.mark.parametrize(
        "instance,json_str",
        [
            pytest.param(full_instance(), FULL_JSON, id="full JSON"),
            pytest.param(
                mosaic_delta_instance(),
                MOSAIC_DELTA_JSON,
                id="mosaic partial configuration",
            ),
        ],
    )
    def test_round_trip(self, instance, json_str):
        assert_json_is_equal(json_str, CODEC.dumps(instance))
        assert instance == CODEC.loads(ReceptorGroup, json_str)

from ska_tmc_cdm import CODEC
from ska_tmc_cdm.messages.subarray_node.configure.receptorgroup import (
    FixedTrajectory,
    Projection,
    ProjectionAlignment,
    ProjectionType,
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

    def test_round_trip(self):
        """
        Test serialisation and deserialisation of a fully-defined
        FixedTrajectory.
        """
        instance = FixedTrajectory(
            attrs=FixedTrajectory.Attrs(x=12.34, y=56.78)
        )
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

    def test_round_trip(self):
        """
        Test serialisation and deserialisation of a fully-defined
        TableTrajectory.
        """
        instance = TableTrajectory(
            attrs=TableTrajectory.Attrs(
                x=[1.1, 2.2, 3.3], y=[4.4, 5.5, 6.6], t=[7.7, 8.8, 9.9]
            )
        )
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

    def test_round_trip(self):
        instance = Projection(
            name=ProjectionType.SSN, alignment=ProjectionAlignment.ICRS
        )
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

from ska_tmc_cdm import CODEC
from ska_tmc_cdm.messages.subarray_node.configure.receptorgroup import (
    FixedTrajectory,
)
from tests.utils import assert_json_is_equal


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

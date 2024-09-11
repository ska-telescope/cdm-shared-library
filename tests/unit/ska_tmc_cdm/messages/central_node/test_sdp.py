"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
from typing import NamedTuple

import pytest

from ska_tmc_cdm.messages.central_node.sdp import PhaseDir
from tests.unit.ska_tmc_cdm.builder.central_node.sdp import PhaseDirBuilder


class PhaseDirCase(NamedTuple):
    equal: bool
    pd1: PhaseDir
    pd2: PhaseDir


PHASEDIR_CASES = (
    PhaseDirCase(
        equal=True,
        pd1=PhaseDirBuilder(),
        pd2=PhaseDirBuilder(),
    ),
    PhaseDirCase(
        equal=True,
        pd1=PhaseDirBuilder(dec=[12.582438888888891]),
        # Very slightly different dec
        pd2=PhaseDirBuilder(dec=[12.582438888888893]),
    ),
    PhaseDirCase(
        equal=False,
        pd1=PhaseDirBuilder(reference_frame="ICRF3"),
        pd2=PhaseDirBuilder(reference_frame="ICRF4"),
    ),
    PhaseDirCase(
        equal=False,
        pd1=PhaseDirBuilder(ra=[123, 0.1]),
        pd2=PhaseDirBuilder(ra=[123, 2.1]),
    ),
)


@pytest.mark.parametrize(
    "expected_equal,phase_dir1,phase_dir2", PHASEDIR_CASES
)
def test_phase_dir_equals(
    expected_equal: bool, phase_dir1: PhaseDir, phase_dir2: PhaseDir
):
    """
    Verify that Phase Dir objects are considered equal when they have:
     - (almost) the same ra
     - (almost) the same dec (we use math.isclose() to allow for floating point math imprecision)
     - the same refrence_time
     - the same refrence_frame
    """
    if expected_equal:
        assert phase_dir1 == phase_dir2
    else:
        assert phase_dir1 != phase_dir2

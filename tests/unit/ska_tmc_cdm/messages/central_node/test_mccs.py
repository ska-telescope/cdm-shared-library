"""
Unit tests for the CentralNode.mccs allocate module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.central_node.mccs import (
    ApertureConfigurationBuilder,
    MCCSAllocateBuilder,
    SubArrayBeamsConfigurationBuilder,
)

test_aperture_config = (
    ApertureConfigurationBuilder()
    .set_aperture_id("AP001.01")
    .set_station_id(1)
    .build()
)
test_subarray_beam_config = (
    SubArrayBeamsConfigurationBuilder()
    .set_subarray_beam_id(1)
    .set_apertures([test_aperture_config])
    .set_number_of_channels(8)
    .build()
)


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        # equal
        (
            MCCSAllocateBuilder(),
            MCCSAllocateBuilder(),
            True,
        ),
        # not equal
        (
            MCCSAllocateBuilder(station_ids=[[1, 2]]),
            MCCSAllocateBuilder(
                station_ids=[[1, 2, 3]]
            ),  # different station id
            False,
        ),
    ],
)
def test_mccs_allocate_eq(object1, object2, is_equal):
    """
    Verify  object  of MCCS Allocate with same properties are equal
    And with different properties are different and also check equality with different object
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()

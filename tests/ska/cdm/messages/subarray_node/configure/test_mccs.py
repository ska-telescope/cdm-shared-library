"""
Unit tests for the ska.cdm.messages.subarray_node.configure.mccs module.
"""

from ska.cdm.messages.subarray_node.configure.mccs import StnConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import StnBeamConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import MCCSConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import MCCSAllocate


def test_stn_configuration_equals():
    """
    Verify that StnConfigurations are considered equal when all attributes are
    equal.
    """
    station_id = 1
    config = StnConfiguration(station_id)
    assert config == StnConfiguration(station_id)
    assert config != StnConfiguration(3)


def test_stn_configuration_not_equal_to_other_objects():
    """
    Verify that StnConfiguration objects are not considered equal to objects
    of other types.
    """
    config = StnConfiguration(1)
    assert config is not None
    assert config != 1
    assert config != object()


def test_stnbeam_configuration_equals():
    """
    Verify that StnBeamConfigurations are considered equal when all attributes are
    equal.
    """
    station_beam_id = 4
    station_ids = [2, 3]
    channels = [5, 6, 7, 8, 9]
    update_rate = 1.5
    sky_coordinates = [0.1, 180.0, 0.5, 45.0, 1.6]
    config = StnBeamConfiguration(
        station_beam_id, station_ids, channels, update_rate, sky_coordinates
    )
    assert config == StnBeamConfiguration(
        station_beam_id, station_ids, channels, update_rate, sky_coordinates
    )
    assert config != StnBeamConfiguration(
        6, station_ids, channels, update_rate, sky_coordinates
    )
    assert config != StnBeamConfiguration(
        station_beam_id, [3, 4], channels, update_rate, sky_coordinates
    )
    assert config != StnBeamConfiguration(
        station_beam_id, station_ids, [1, 2, 3, 4, 5, 6], update_rate, sky_coordinates
    )
    assert config != StnBeamConfiguration(
        station_beam_id, station_ids, channels, 4.5, sky_coordinates
    )
    assert config != StnBeamConfiguration(
        station_beam_id,
        station_ids,
        channels,
        update_rate,
        [0.1, 182.0, 0.5, 45.0, 1.6],
    )


def test_stnbeam_configuration_not_equal_to_other_objects():
    """
    Verify that StnBeamConfiguration objects are not considered equal to objects
    of other types.
    """
    config = StnBeamConfiguration(
        1, [1, 2], [1, 2, 3, 4, 5, 6], 1.0, [0.1, 182.0, 0.5, 45.0, 1.6]
    )
    assert config is not None
    assert config != 1
    assert config != object()


def test_mccs_configuration_equals():
    """
    Verify that MCCSConfiguration objects are considered equal when all
    attributes are equal.
    """
    station_config = StnConfiguration(1)
    station_beam_config = StnBeamConfiguration(
        1, [1, 2], [1, 2, 3, 4, 5, 6], 1.0, [0.1, 182.0, 0.5, 45.0, 1.6]
    )

    config = MCCSConfiguration([station_config], [station_beam_config])
    assert config == MCCSConfiguration([station_config], [station_beam_config])
    assert config != MCCSConfiguration([StnConfiguration(2)], [station_beam_config])
    assert config != MCCSConfiguration(
        [station_config],
        [
            StnBeamConfiguration(
                4, [1, 2], [1, 2, 3, 4, 5, 6], 1.0, [0.1, 182.0, 0.5, 45.0, 1.6]
            )
        ],
    )


def test_mccs_config_not_equal_to_other_objects():
    """
    Verify that MCCSConfiguration objects are not considered equal to objects
    of other types.
    """
    station_config = StnConfiguration(1)
    station_beam_config = StnBeamConfiguration(
        1, [1, 2], [1, 2, 3, 4, 5, 6], 1.0, [0.1, 182.0, 0.5, 45.0, 1.6]
    )

    config = MCCSConfiguration([station_config], [station_beam_config])
    assert config is not None
    assert config != 1
    assert config != object()


def test_mccs_allocate_eq():
    """
    Verify that two MCCSAllocate objects with the same allocated elements are
    considered equal.
    """
    mccs_allocate = MCCSAllocate(
        [1, 2, 3, 4], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate == MCCSAllocate(
        [1, 2, 3, 4], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate != MCCSAllocate(
        [2, 3, 4, 5], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate != MCCSAllocate(
        [2, 3, 4], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate != MCCSAllocate(
        [1, 2, 3, 4], [[3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate != MCCSAllocate(
        [1, 2, 3, 4], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7]
    )


def test_mccs_allocate_eq_with_other_objects():
    """
    Verify that a MCCSAllocate is considered unequal to objects of other
    types.
    """
    mccs_allocate = MCCSAllocate(
        [1, 2, 3, 4], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate != 1
    assert mccs_allocate != object()

def test_mccs_allocate_is_empty():
    """
    Verify that we can detect an empty MCCSAllocate
    """
    mccs_allocate = MCCSAllocate([],[],[])
    
    assert mccs_allocate.is_empty()

def test_mccs_allocate_is_not_empty():
    """
    Verify that we can detect an MCCSAllocate is not empty
    """
    mccs_allocate = MCCSAllocate(
        [1, 2, 3, 4], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    
    assert not mccs_allocate.is_empty()
    
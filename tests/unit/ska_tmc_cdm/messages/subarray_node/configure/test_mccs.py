"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.mccs module.
"""

from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamConfiguration,
    SubarrayBeamTarget,
)


def test_subarray_beam_target_equals():
    """
    Verify that SubarrayBeamConfiguration are considered equal when all attributes are
    equal.
    """
    az = 180.0
    el = 45.0
    target_name = "DriftScan"
    reference_frame = "horizon"

    config = SubarrayBeamTarget(az, el, target_name, reference_frame)
    assert config == SubarrayBeamTarget(az, el, target_name, reference_frame)
    assert config != SubarrayBeamTarget(az, el, "target_name", "reference_frame")


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
    Verify that SubarrayBeamConfigurations are considered equal when all attributes are
    equal.
    """
    subarray_beam_id = 4
    station_ids = [2, 3]
    channels = [[5, 6, 7, 8, 9]]
    update_rate = 1.5
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    antenna_weights = [1.0, 1.0, 1.0]
    phase_centre = [0.0, 0.0]
    station_beam_config = SubarrayBeamConfiguration(
        subarray_beam_id,
        station_ids,
        channels,
        update_rate,
        target,
        antenna_weights,
        phase_centre,
    )
    config = station_beam_config
    config1 = station_beam_config
    assert config == config1

    assert config != SubarrayBeamConfiguration(
        6, station_ids, channels, update_rate, target, antenna_weights, phase_centre
    )
    assert config != SubarrayBeamConfiguration(
        subarray_beam_id,
        [3, 4],
        channels,
        update_rate,
        target,
        antenna_weights,
        phase_centre,
    )
    assert config != SubarrayBeamConfiguration(
        subarray_beam_id,
        station_ids,
        [[1, 2, 3, 4, 5, 6]],
        update_rate,
        target,
        antenna_weights,
        phase_centre,
    )
    assert config != SubarrayBeamConfiguration(
        subarray_beam_id,
        station_ids,
        channels,
        4.5,
        target,
        antenna_weights,
        phase_centre,
    )
    assert config != SubarrayBeamConfiguration(
        subarray_beam_id,
        station_ids,
        channels,
        update_rate,
        SubarrayBeamTarget(190.0, 45.0, "DriftScan", "HORIZON"),
        antenna_weights,
        phase_centre,
    )

    assert config != SubarrayBeamConfiguration(
        subarray_beam_id,
        station_ids,
        channels,
        update_rate,
        target,
        [2.0, 2.0, 2.0],
        phase_centre,
    )

    assert config != SubarrayBeamConfiguration(
        subarray_beam_id,
        station_ids,
        channels,
        update_rate,
        target,
        antenna_weights,
        [1.0, 1.0],
    )


def test_stnbeam_configuration_not_equal_to_other_objects():
    """
    Verify that SubarrayBeamConfiguration objects are not considered equal to objects
    of other types.
    """
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    config = SubarrayBeamConfiguration(
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    assert config is not None
    assert config != 1
    assert config != object()


def test_mccs_configuration_equals():
    """
    Verify that MCCSConfiguration objects are considered equal when all
    attributes are equal.
    """
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    station_config = StnConfiguration(1)
    subarray_beam_config = SubarrayBeamConfiguration(
        subarray_beam_id=1,
        station_ids=[1, 2],
        channels=[[1, 2, 3, 4, 5, 6]],
        update_rate=1.0,
        target=target,
        antenna_weights=[1.0, 1.0, 1.0],
        phase_centre=[0.0, 0.0],
    )
    config = MCCSConfiguration(
        station_configs=[station_config], subarray_beam_configs=[subarray_beam_config]
    )
    assert config == MCCSConfiguration(
        station_configs=[station_config], subarray_beam_configs=[subarray_beam_config]
    )
    assert config != MCCSConfiguration(
        station_configs=[StnConfiguration(2)],
        subarray_beam_configs=[subarray_beam_config],
    )
    assert config != MCCSConfiguration(
        station_configs=[station_config],
        subarray_beam_configs=[
            SubarrayBeamConfiguration(
                subarray_beam_id=4,
                station_ids=[1, 2],
                channels=[[1, 2, 3, 4, 5, 6]],
                update_rate=1.0,
                target=target,
                antenna_weights=[1.0, 1.0, 1.0],
                phase_centre=[0.0, 0.0],
            )
        ],
    )


def test_mccs_config_not_equal_to_other_objects():
    """
    Verify that MCCSConfiguration objects are not considered equal to objects
    of other types.
    """
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    station_config = StnConfiguration(1)
    station_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    )

    config = MCCSConfiguration(
        station_configs=[station_config], subarray_beam_configs=[station_beam_config]
    )
    assert config is not None
    assert config != 1
    assert config != object()

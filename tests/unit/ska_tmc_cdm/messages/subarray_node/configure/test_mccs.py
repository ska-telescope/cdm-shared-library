"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.mccs module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.mccs import (
    MCCSConfigurationBuilder,
    StnConfigurationBuilder,
    SubarrayBeamConfigurationBuilder,
    SubarrayBeamTargetBuilder,
)


@pytest.mark.parametrize(
    "subarray_beam_target_a, subarray_beam_target_b, is_equal",
    [
        (
            SubarrayBeamTargetBuilder()
            .set_az(180.0)
            .set_el(45.0)
            .set_target_name("DriftScan")
            .set_reference_frame("horizon")
            .build(),
            SubarrayBeamTargetBuilder()
            .set_az(180.0)
            .set_el(45.0)
            .set_target_name("DriftScan")
            .set_reference_frame("horizon")
            .build(),
            True,
        ),
        (
            SubarrayBeamTargetBuilder()
            .set_az(180.0)
            .set_el(45.0)
            .set_target_name("DriftScan")
            .set_reference_frame("horizon")
            .build(),
            SubarrayBeamTargetBuilder()
            .set_az(180.0)
            .set_el(45.0)
            .set_target_name("target_name")
            .set_reference_frame("reference_frame")
            .build(),
            False,
        ),
    ],
)
def test_subarray_beam_target_equality(
    subarray_beam_target_a, subarray_beam_target_b, is_equal
):
    """
    Verify that SubarrayBeamTarget objects are equal when they have the same values, not equal for different value
    and not equal when any attribute differs.
    """
    assert (subarray_beam_target_a == subarray_beam_target_b) == is_equal
    assert subarray_beam_target_a != 1
    assert subarray_beam_target_b != object


@pytest.mark.parametrize(
    "stn_config_a, stn_config_b, is_equal",
    [
        (
            StnConfigurationBuilder().set_station_id(1).build(),
            StnConfigurationBuilder().set_station_id(1).build(),
            True,
        ),
        (
            StnConfigurationBuilder().set_station_id(1).build(),
            StnConfigurationBuilder().set_station_id(3).build(),
            False,
        ),
    ],
)
def test_stn_configuration_equality(stn_config_a, stn_config_b, is_equal):
    """
    Verify that StnConfiguration objects are equal when they have the same station_id
    and not equal when station_ids are different or compared to different types.
    """
    assert (stn_config_a == stn_config_b) == is_equal
    assert stn_config_a != 1
    assert stn_config_b != object()


@pytest.mark.parametrize(
    "station_beam_config_b, is_equal",
    [
        (
            SubarrayBeamConfigurationBuilder()
            .set_subarray_beam_id(1)
            .set_station_ids([1, 2])
            .set_channels([[1, 2, 3, 4, 5, 6]])
            .set_update_rate(1.0)
            .set_target(
                SubarrayBeamTargetBuilder()
                .set_az(180.0)
                .set_el(45.0)
                .set_target_name("DriftScan")
                .set_reference_frame("HORIZON")
                .build()
            )
            .set_antenna_weights([1.0, 1.0, 1.0])
            .set_phase_centre([0.0, 0.0])
            .build(),
            True,
        ),
        (
            SubarrayBeamConfigurationBuilder()
            .set_subarray_beam_id(2)  # Different ID
            .set_station_ids([1, 2])
            .set_channels([[1, 2, 3, 4, 5, 6]])
            .set_update_rate(1.0)
            .set_target(
                SubarrayBeamTargetBuilder()
                .set_az(180.0)
                .set_el(45.0)
                .set_target_name("DriftScan")
                .set_reference_frame("HORIZON")
                .build()
            )
            .set_antenna_weights([1.0, 1.0, 1.0])
            .set_phase_centre([0.0, 0.0])
            .build(),
            False,
        ),
        # Different station_ids
        (
            SubarrayBeamConfigurationBuilder()
            .set_subarray_beam_id(1)
            .set_station_ids([3, 4])
            .set_channels([[1, 2, 3, 4, 5, 6]])
            .set_update_rate(1.0)
            .set_target(
                SubarrayBeamTargetBuilder()
                .set_az(180.0)
                .set_el(45.0)
                .set_target_name("DriftScan")
                .set_reference_frame("HORIZON")
                .build()
            )
            .set_antenna_weights([1.0, 1.0, 1.0])
            .set_phase_centre([0.0, 0.0])
            .build(),
            False,
        ),
        # Different channels
        (
            SubarrayBeamConfigurationBuilder()
            .set_subarray_beam_id(1)
            .set_station_ids([1, 2])
            .set_channels(
                [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]]
            )  # Different channels
            .set_update_rate(1.0)
            .set_target(
                SubarrayBeamTargetBuilder()
                .set_az(180.0)
                .set_el(45.0)
                .set_target_name("DriftScan")
                .set_reference_frame("HORIZON")
                .build()
            )
            .set_antenna_weights([1.0, 1.0, 1.0])
            .set_phase_centre([0.0, 0.0])
            .build(),
            False,
        ),
        # Different update_rate
        (
            SubarrayBeamConfigurationBuilder()
            .set_subarray_beam_id(1)
            .set_station_ids([1, 2])
            .set_channels([[1, 2, 3, 4, 5, 6]])
            .set_update_rate(2.0)  # Different update_rate
            .set_target(
                SubarrayBeamTargetBuilder()
                .set_az(180.0)
                .set_el(45.0)
                .set_target_name("DriftScan")
                .set_reference_frame("HORIZON")
                .build()
            )
            .set_antenna_weights([1.0, 1.0, 1.0])
            .set_phase_centre([0.0, 0.0])
            .build(),
            False,
        ),
        # Different target
        (
            SubarrayBeamConfigurationBuilder()
            .set_subarray_beam_id(1)
            .set_station_ids([1, 2])
            .set_channels([[1, 2, 3, 4, 5, 6]])
            .set_update_rate(1.0)
            .set_target(
                SubarrayBeamTargetBuilder()
                .set_az(90.0)  # Different target
                .set_el(45.0)
                .set_target_name("DriftScan")
                .set_reference_frame("HORIZON")
                .build()
            )
            .set_antenna_weights([1.0, 1.0, 1.0])
            .set_phase_centre([0.0, 0.0])
            .build(),
            False,
        ),
        # Different antenna_weights
        (
            SubarrayBeamConfigurationBuilder()
            .set_subarray_beam_id(1)
            .set_station_ids([1, 2])
            .set_channels([[1, 2, 3, 4, 5, 6]])
            .set_update_rate(1.0)
            .set_target(
                SubarrayBeamTargetBuilder()
                .set_az(180.0)
                .set_el(45.0)
                .set_target_name("DriftScan")
                .set_reference_frame("HORIZON")
                .build()
            )
            .set_antenna_weights([2.0, 2.0, 2.0])
            .set_phase_centre([0.0, 0.0])
            .build(),
            False,
        ),
        # Different phase_centre
        (
            SubarrayBeamConfigurationBuilder()
            .set_subarray_beam_id(1)
            .set_station_ids([1, 2])
            .set_channels([[1, 2, 3, 4, 5, 6]])
            .set_update_rate(1.0)
            .set_target(
                SubarrayBeamTargetBuilder()
                .set_az(180.0)
                .set_el(45.0)
                .set_target_name("DriftScan")
                .set_reference_frame("HORIZON")
                .build()
            )
            .set_antenna_weights([2.0, 2.0, 2.0])
            .set_phase_centre([1.0, 1.0])  # Different phase_centre
            .build(),
            False,
        ),
    ],
)
def test_subarray_beam_configuration_equality(
    station_beam_config, station_beam_config_b, is_equal
):
    """
    Verify that SubarrayBeamConfiguration objects are considered equal or not equal as expected.
    """
    assert (station_beam_config == station_beam_config_b) == is_equal
    assert station_beam_config != 1
    assert station_beam_config != object()


@pytest.mark.parametrize(
    "mccs_config_a, mccs_config_b, is_equal",
    [
        (
            MCCSConfigurationBuilder()
            .set_station_configs([StnConfigurationBuilder().set_station_id(1).build()])
            .set_subarray_beam_config(
                [
                    SubarrayBeamConfigurationBuilder()
                    .set_subarray_beam_id(1)
                    .set_station_ids([1, 2])
                    .set_channels([[1, 2, 3, 4, 5, 6]])
                    .set_update_rate(1.0)
                    .set_target(
                        SubarrayBeamTargetBuilder()
                        .set_az(180.0)
                        .set_el(45.0)
                        .set_target_name("DriftScan")
                        .set_reference_frame("HORIZON")
                        .build()
                    )
                    .set_antenna_weights([1.0, 1.0, 1.0])
                    .set_phase_centre([0.0, 0.0])
                    .build()
                ]
            )
            .build(),
            MCCSConfigurationBuilder()
            .set_station_configs([StnConfigurationBuilder().set_station_id(1).build()])
            .set_subarray_beam_config(
                [
                    SubarrayBeamConfigurationBuilder()
                    .set_subarray_beam_id(1)
                    .set_station_ids([1, 2])
                    .set_channels([[1, 2, 3, 4, 5, 6]])
                    .set_update_rate(1.0)
                    .set_target(
                        SubarrayBeamTargetBuilder()
                        .set_az(180.0)
                        .set_el(45.0)
                        .set_target_name("DriftScan")
                        .set_reference_frame("HORIZON")
                        .build()
                    )
                    .set_antenna_weights([1.0, 1.0, 1.0])
                    .set_phase_centre([0.0, 0.0])
                    .build()
                ]
            )
            .build(),
            True,
        ),
        (
            MCCSConfigurationBuilder()
            .set_station_configs([StnConfigurationBuilder().set_station_id(1).build()])
            .set_subarray_beam_config(
                [
                    SubarrayBeamConfigurationBuilder()
                    .set_subarray_beam_id(1)
                    .set_station_ids([1, 2])
                    .set_channels([[1, 2, 3, 4, 5, 6]])
                    .set_update_rate(1.0)
                    .set_target(
                        SubarrayBeamTargetBuilder()
                        .set_az(180.0)
                        .set_el(45.0)
                        .set_target_name("DriftScan")
                        .set_reference_frame("HORIZON")
                        .build()
                    )
                    .set_antenna_weights([1.0, 1.0, 1.0])
                    .set_phase_centre([0.0, 0.0])
                    .build()
                ]
            )
            .build(),
            MCCSConfigurationBuilder()
            .set_station_configs([StnConfigurationBuilder().set_station_id(1).build()])
            .set_subarray_beam_config(
                [
                    SubarrayBeamConfigurationBuilder()
                    .set_subarray_beam_id(1)
                    .set_station_ids([1, 2])
                    .set_channels([[1, 2, 3, 4, 5, 6]])
                    .set_update_rate(1.0)
                    .set_target(
                        SubarrayBeamTargetBuilder()
                        .set_az(90.0)  # changed az value
                        .set_el(45.0)
                        .set_target_name("DriftScan")
                        .set_reference_frame("HORIZON")
                        .build()
                    )
                    .set_antenna_weights([1.0, 1.0, 1.0])
                    .set_phase_centre([0.0, 0.0])
                    .build()
                ]
            )
            .build(),
            False,
        ),
    ],
)
def test_mccs_configuration_equality(mccs_config_a, mccs_config_b, is_equal):
    """
    Verify MCCSConfiguration objects are equal when all attributes match,
    and not equal when there's any difference in their attributes.
    """
    assert (mccs_config_a == mccs_config_b) == is_equal
    assert mccs_config_a != 1
    assert mccs_config_b != object

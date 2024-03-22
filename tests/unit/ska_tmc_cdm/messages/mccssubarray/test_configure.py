"""
Unit tests for the ska_tmc_cdm.messages.mccssubarray.configure module.
"""

from ska_tmc_cdm.messages.mccssubarray.configure import (
    ConfigureRequest,
    StationConfiguration,
    SubarrayBeamAperatures,
    SubarrayBeamConfiguration,
    SubarrayBeamLogicalBands,
    SubarrayBeamSkyCoordinates,
)


def test_stationconfiguration_object_equality():
    """
    Verify that StationConfigurations are considered equal when all attributes are
    equal.
    """
    station_id = 1
    config = StationConfiguration(station_id)
    assert config == StationConfiguration(station_id)
    assert config != StationConfiguration(3)


def test_stationconfiguration_not_equal_to_other_objects():
    """
    Verify that StationConfiguration objects are not considered equal to objects
    of other types.
    """
    config = StationConfiguration(1)
    assert config is not None
    assert config != 1
    assert config != object()


def test_subarraybeamconfiguration_object_equality():
    """
    Verify that SubarrayBeamConfigurations are considered equal when all
    attributes are equal.
    """
    constructor_args = dict(
        subarray_beam_id=1,
        station_ids=[2, 3],
        channels=[[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 1]],
        update_rate=1.5,
        antenna_weights=[1.0, 1.0, 1.0],
        phase_centre=[0.0, 0.0],
        logical_bands=[
            SubarrayBeamLogicalBands(start_channel=80, number_of_channels=16)
        ],
        apertures=[
            SubarrayBeamAperatures(
                aperture_id="AP001.01", weighting_key_ref="aperture2"
            )
        ],
        sky_coordinates=SubarrayBeamSkyCoordinates(
            timestamp="2021-10-23T12:34:56.789Z",
            reference_frame="ICRS",
            c1=180.0,
            c1_rate=0.5,
            c2=45.0,
            c2_rate=1.6,
        ),
    )
    config = SubarrayBeamConfiguration(**constructor_args)

    # objects with same property values are considered equal
    other = SubarrayBeamConfiguration(**constructor_args)
    assert config == other

    alternate_args = dict(
        subarray_beam_id=2,
        station_ids=[7, 8],
        channels=[
            [0, 8, 1, 1],
            [8, 8, 2, 1],
        ],
        update_rate=2.5,
        antenna_weights=[0.8, 1.0],
        phase_centre=[0.1, 0.1],
        logical_bands=[
            SubarrayBeamLogicalBands(start_channel=82, number_of_channels=17)
        ],
        apertures=[
            SubarrayBeamAperatures(
                aperture_id="AP001.02", weighting_key_ref="aperture3"
            )
        ],
        sky_coordinates=SubarrayBeamSkyCoordinates(
            timestamp="2021-10-23T12:34:56.789Z",
            reference_frame="ICRS",
            c1=180.0,
            c1_rate=0.5,
            c2=45.0,
            c2_rate=1.5,
        ),
    )
    for k, v in alternate_args.items():
        other_args = dict(constructor_args)
        other_args[k] = v
        assert config != SubarrayBeamConfiguration(**other_args)


def test_subarraybeam_configuration_not_equal_to_other_objects():
    """
    Verify that SubarrayBeamConfiguration objects are not considered equal to objects
    of other types.
    """
    constructor_args = dict(
        subarray_beam_id=1,
        station_ids=[2, 3],
        channels=[[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 1]],
        update_rate=1.5,
        antenna_weights=[1.0, 1.0, 1.0],
        phase_centre=[0.0, 0.0],
        logical_bands=[
            SubarrayBeamLogicalBands(start_channel=80, number_of_channels=16)
        ],
        apertures=[
            SubarrayBeamAperatures(
                aperture_id="AP001.01", weighting_key_ref="aperture2"
            )
        ],
        sky_coordinates=SubarrayBeamSkyCoordinates(
            timestamp="2021-10-23T12:34:56.789Z",
            reference_frame="ICRS",
            c1=180.0,
            c1_rate=0.5,
            c2=45.0,
            c2_rate=1.6,
        ),
    )
    config = SubarrayBeamConfiguration(**constructor_args)

    assert config != 1
    assert config != object()


def test_configurerequest_equals():
    """
    Verify that ConfigureRequest objects are considered equal when all
    attributes are equal.
    """
    station_configs = [
        StationConfiguration(1),
        StationConfiguration(2),
    ]
    subarray_beam_config = SubarrayBeamConfiguration(
        subarray_beam_id=1,
        station_ids=[1, 2],
        channels=[[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 1]],
        update_rate=1.5,
        antenna_weights=[1.0, 1.0],
        phase_centre=[0.0, 0.0],
        logical_bands=[
            SubarrayBeamLogicalBands(start_channel=80, number_of_channels=16)
        ],
        apertures=[
            SubarrayBeamAperatures(
                aperture_id="AP001.01", weighting_key_ref="aperture2"
            )
        ],
        sky_coordinates=SubarrayBeamSkyCoordinates(
            timestamp="2021-10-23T12:34:56.789Z",
            reference_frame="ICRS",
            c1=180.0,
            c1_rate=0.5,
            c2=45.0,
            c2_rate=1.6,
        ),
    )

    request = ConfigureRequest(
        stations=station_configs, subarray_beams=[subarray_beam_config]
    )

    other = ConfigureRequest(
        stations=station_configs, subarray_beams=[subarray_beam_config]
    )
    assert request == other

    other = ConfigureRequest(
        stations=station_configs[1:], subarray_beams=[subarray_beam_config]
    )
    assert request != other

    other = ConfigureRequest(stations=station_configs, subarray_beams=[])
    assert request != other


def test_configurerequest_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest objects are not considered equal to objects
    of other types.
    """
    station_configs = [
        StationConfiguration(1),
        StationConfiguration(2),
    ]
    subarray_beam_config = SubarrayBeamConfiguration(
        subarray_beam_id=1,
        station_ids=[1, 2],
        channels=[[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 1]],
        update_rate=1.5,
        antenna_weights=[1.0, 1.0],
        phase_centre=[0.0, 0.0],
        logical_bands=[
            SubarrayBeamLogicalBands(start_channel=80, number_of_channels=16)
        ],
        apertures=[
            SubarrayBeamAperatures(
                aperture_id="AP001.01", weighting_key_ref="aperture2"
            )
        ],
        sky_coordinates=SubarrayBeamSkyCoordinates(
            timestamp="2021-10-23T12:34:56.789Z",
            reference_frame="ICRS",
            c1=180.0,
            c1_rate=0.5,
            c2=45.0,
            c2_rate=1.6,
        ),
    )

    request = ConfigureRequest(
        stations=station_configs, subarray_beams=[subarray_beam_config]
    )

    assert request != 1
    assert request != object()

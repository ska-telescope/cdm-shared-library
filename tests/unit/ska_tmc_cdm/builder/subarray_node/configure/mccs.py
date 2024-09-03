import functools

from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    SubarrayBeamAperatures,
    SubarrayBeamConfiguration,
    SubarrayBeamLogicalBands,
    SubarrayBeamSkyCoordinates,
)

SubarrayBeamSkyCoordinatesBuilder = functools.partial(
    SubarrayBeamSkyCoordinates, reference_frame="HORIZON", c1=180.0, c2=90.0
)


SubarrayBeamLogicalbandsBuilder = functools.partial(
    SubarrayBeamLogicalBands,
    start_channel=80,
    number_of_channels=16,
)


SubarrayBeamApertureBuilder = functools.partial(
    SubarrayBeamAperatures,
    aperture_id="AP001.01",
    weighting_key_ref="aperture2",
)


SubarrayBeamConfigurationBuilder = functools.partial(
    SubarrayBeamConfiguration,
    subarray_beam_id=1,
    update_rate=1.0,
    logical_bands=(SubarrayBeamLogicalbandsBuilder(),),
    apertures=(SubarrayBeamApertureBuilder(),),
    sky_coordinates=SubarrayBeamSkyCoordinatesBuilder(),
)


MCCSConfigurationBuilder = functools.partial(MCCSConfiguration)

import functools

from ska_tmc_cdm.messages.central_node.mccs import (
    ApertureConfiguration,
    MCCSAllocate,
    SubArrayBeamsConfiguration,
)

ApertureConfigurationBuilder = functools.partial(
    ApertureConfiguration, aperture_id="AP001.01", station_id=1
)


SubArrayBeamsConfigurationBuilder = functools.partial(
    SubArrayBeamsConfiguration,
    subarray_beam_id=1,
    number_of_channels=8,
    apertures=(ApertureConfigurationBuilder(),),
)


MCCSAllocateBuilder = functools.partial(
    MCCSAllocate,
    subarray_beam_ids=(1,),
    station_ids=((1, 2),),
    channel_blocks=(3,),
)

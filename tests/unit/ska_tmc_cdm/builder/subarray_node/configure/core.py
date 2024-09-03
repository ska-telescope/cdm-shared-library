import functools

from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    PointingConfiguration,
    ReceiverBand,
    SolarSystemObject,
    SpecialTarget,
    Target,
)

SpecialTargetBuilder = functools.partial(
    SpecialTarget, target_name=SolarSystemObject.SUN
)

TargetBuilder = functools.partial(
    Target,
    ra=1,
    dec=1,
    ca_offset_arcsec=5.0,
    ie_offset_arcsec=5.0,
)


PointingConfigurationBuilder = functools.partial(
    PointingConfiguration, target=TargetBuilder()
)


DishConfigurationBuilder = functools.partial(
    DishConfiguration, receiver_band=ReceiverBand.BAND_1
)

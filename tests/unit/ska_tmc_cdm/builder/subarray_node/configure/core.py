import functools

from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    HolographyReceptorGroupConfig,
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

HolographyReceptorGroupConfigBuilder = functools.partial(
    HolographyReceptorGroupConfig,
    receptors=["SKA001", "SKA002", "SKA003"],
    field={
        "target_name": "Cen-A",
        "reference_frame": "ICRS",
        "attrs": {
            "c1": 201.365,
            "c2": -43.0191667,
        },
    },
    projection={"name": "SSN", "alignment": "ICRS"},
)

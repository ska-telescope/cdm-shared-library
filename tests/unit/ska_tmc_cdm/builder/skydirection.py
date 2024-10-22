import functools

from ska_tmc_cdm.messages.skydirection import (
    AltAzField,
    GalacticField,
    ICRSField,
    SolarSystemObject,
    SpecialField,
)

ICRSFieldBuilder = functools.partial(
    ICRSField,
    target_name="PSR J0024-7204R",
    attrs=ICRSField.Attrs(c1=6.023625, c2=-72.08128333, pm_c1=4.8, pm_c2=-3.3),
)

GalacticFieldBuilder = functools.partial(
    GalacticField,
    target_name="PSR J0024-7204R",
    attrs=GalacticField.Attrs(
        c1=6.023625, c2=-72.08128333, pm_c1=4.8, pm_c2=-3.3
    ),
)

AltAzFieldBuilder = functools.partial(
    AltAzField,
    target_name="Zenith",
    attrs=AltAzField.Attrs(c1=0.0, c2=90.0),
)

SpecialFieldBuilder = functools.partial(
    SpecialField, target_name=SolarSystemObject.SATURN
)

"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure.mccs module.
"""
import pytest

from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    SubarrayBeamAperatures,
    SubarrayBeamConfiguration,
    SubarrayBeamLogicalBands,
    SubarrayBeamSkyCoordinates,
)
from ska_tmc_cdm.schemas.subarray_node.configure.mccs import (
    MCCSConfigurationSchema,
    SubarrayBeamConfigurationSchema,
)
from ska_tmc_cdm.utils import assert_json_is_equal

VALID_LOGICAL_BANDS_JSON = """
[{
"start_channel": 80,
"number_of_channels": 16
}
],
"""

VALID_APERTURES_JSON = """
 [
          {
            "aperture_id": "AP001.01",
            "weighting_key_ref": "aperture2"
          }
],
"""
VALID_SKY_COORDINATES_JSON = """
{
          "reference_frame": "ICRS",
          "c1": 180.0,
          "c2": 45.0
}
"""

VALID_SUBARRAYBEAMCONFIGURATION_JSON = (
    """
{
    "subarray_beam_id": 1,
    "update_rate": 0.0,
    "logical_bands":"""
    + VALID_LOGICAL_BANDS_JSON
    + """
    "apertures":"""
    + VALID_APERTURES_JSON
    + """
    "sky_coordinates":"""
    + VALID_SKY_COORDINATES_JSON
    + """
}
"""
)

VALID_SUBARRAYBEAMCONFIGURATION_OBJECT = SubarrayBeamConfiguration(
    subarray_beam_id=1,
    update_rate=0.0,
    logical_bands=[SubarrayBeamLogicalBands(start_channel=80, number_of_channels=16)],
    apertures=[
        SubarrayBeamAperatures(aperture_id="AP001.01", weighting_key_ref="aperture2")
    ],
    sky_coordinates=SubarrayBeamSkyCoordinates(
        reference_frame="ICRS",
        c1=180.0,
        c2=45.0,
    ),
)

VALID_MCCSCONFIGURATION_JSON = (
    """
{
    "subarray_beams": [
    """
    + VALID_SUBARRAYBEAMCONFIGURATION_JSON
    + """
    ]
}
"""
)

VALID_MCCSCONFIGURATION_OBJECT = MCCSConfiguration(
    subarray_beam_configs=[VALID_SUBARRAYBEAMCONFIGURATION_OBJECT],
)


@pytest.mark.parametrize(
    "schema_cls,instance,expected",
    [
        (
            SubarrayBeamConfigurationSchema,
            VALID_SUBARRAYBEAMCONFIGURATION_OBJECT,
            VALID_SUBARRAYBEAMCONFIGURATION_JSON,
        ),
        (
            MCCSConfigurationSchema,
            VALID_MCCSCONFIGURATION_OBJECT,
            VALID_MCCSCONFIGURATION_JSON,
        ),
    ],
)
def test_marshal(schema_cls, instance, expected):
    """
    Verify that instances are marshalled to JSON correctly.
    """
    schema = schema_cls()
    marshalled = schema.dumps(instance)
    assert_json_is_equal(expected, marshalled)


@pytest.mark.parametrize(
    "schema_cls,json_str,expected",
    [
        (
            SubarrayBeamConfigurationSchema,
            VALID_SUBARRAYBEAMCONFIGURATION_JSON,
            VALID_SUBARRAYBEAMCONFIGURATION_OBJECT,
        ),
        (
            MCCSConfigurationSchema,
            VALID_MCCSCONFIGURATION_JSON,
            VALID_MCCSCONFIGURATION_OBJECT,
        ),
    ],
)
def test_unmarshal(schema_cls, json_str, expected):
    """
    Verify that instances are unmarshalled to instances correctly.
    """
    schema = schema_cls()
    unmarshalled = schema.loads(json_str)
    assert unmarshalled == expected

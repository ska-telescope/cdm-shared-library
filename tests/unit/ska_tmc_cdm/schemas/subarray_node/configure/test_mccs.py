"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure.mccs module.
"""
import pytest

from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamAperatures,
    SubarrayBeamConfiguration,
    SubarrayBeamLogicalBands,
    SubarrayBeamSkyCoordinates,
    SubarrayBeamTarget,
)
from ska_tmc_cdm.schemas.subarray_node.configure.mccs import (
    MCCSConfigurationSchema,
    StnConfigurationSchema,
    SubarrayBeamConfigurationSchema,
    SubarrayBeamTargetSchema,
)
from ska_tmc_cdm.utils import assert_json_is_equal

VALID_SUBARRAYBEAMTARGET_JSON = """
{
    "reference_frame": "HORIZON",
    "target_name": "DriftScan",
    "az": 180.0,
    "el": 45.0
}
"""

VALID_SUBARRAYBEAMTARGET_OBJECT = SubarrayBeamTarget(
    180.0, 45.0, "DriftScan", "HORIZON"
)

VALID_STNCONFIGURATION_JSON = """
{
    "station_id":1
}
"""

VALID_STNCONFIGURATION_OBJECT = StnConfiguration(1)

VALID_SUBARRAYBEAMCONFIGURATION_JSON = (
    """
{
    "subarray_beam_id": 1,
    "station_ids": [1,2],
    "channels": [[1, 2]],
    "update_rate": 0.0,
    "antenna_weights": [1.0, 1.0, 1.0],
    "phase_centre": [0.0, 0.0],
    "target": """
    + VALID_SUBARRAYBEAMTARGET_JSON
    + """
}
"""
)

VALID_SUBARRAYBEAMCONFIGURATION_OBJECT = SubarrayBeamConfiguration(
    subarray_beam_id=1,
    station_ids=[1, 2],
    channels=[[1, 2]],
    update_rate=0.0,
    target=VALID_SUBARRAYBEAMTARGET_OBJECT,
    antenna_weights=[1.0, 1.0, 1.0],
    phase_centre=[0.0, 0.0],
    logical_bands=[SubarrayBeamLogicalBands(start_channel=80, number_of_channels=16)],
    apertures=[
        SubarrayBeamAperatures(aperture_id="AP001.01", weighting_key_ref="aperture2")
    ],
    sky_coordinates=SubarrayBeamSkyCoordinates(
        "2021-10-23T12:34:56.789Z",
        "ICRS",
        180.0,
        0.0,
        45.0,
        0.0,
    ),
)

VALID_MCCSCONFIGURATION_JSON = (
    """
{
    "stations": [
    """
    + VALID_STNCONFIGURATION_JSON
    + """
    ],
    "subarray_beams": [
    """
    + VALID_SUBARRAYBEAMCONFIGURATION_JSON
    + """
    ]
}
"""
)

VALID_MCCSCONFIGURATION_OBJECT = MCCSConfiguration(
    station_configs=[VALID_STNCONFIGURATION_OBJECT],
    subarray_beam_configs=[VALID_SUBARRAYBEAMCONFIGURATION_OBJECT],
)


@pytest.mark.parametrize(
    "schema_cls,instance,expected",
    [
        (
            SubarrayBeamTargetSchema,
            VALID_SUBARRAYBEAMTARGET_OBJECT,
            VALID_SUBARRAYBEAMTARGET_JSON,
        ),
        (
            StnConfigurationSchema,
            VALID_STNCONFIGURATION_OBJECT,
            VALID_STNCONFIGURATION_JSON,
        ),
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
            SubarrayBeamTargetSchema,
            VALID_SUBARRAYBEAMTARGET_JSON,
            VALID_SUBARRAYBEAMTARGET_OBJECT,
        ),
        (
            StnConfigurationSchema,
            VALID_STNCONFIGURATION_JSON,
            VALID_STNCONFIGURATION_OBJECT,
        ),
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

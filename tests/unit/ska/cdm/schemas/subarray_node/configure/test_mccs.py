"""
Unit tests for the ska.cdm.schemas.subarray_node.configure.mccs module.
"""
import pytest

from ska.cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamConfiguration,
    SubarrayBeamTarget
)
from ska.cdm.schemas.subarray_node.configure.mccs import (
    MCCSConfigurationSchema,
    StnConfigurationSchema,
    SubarrayBeamConfigurationSchema,
    SubarrayBeamTargetSchema
)
from ska.cdm.utils import json_is_equal

VALID_SUBARRAYBEAMTARGET_JSON = """
{
    "system": "HORIZON",
    "name": "DriftScan",
    "az": 180.0,
    "el": 45.0
}
"""

VALID_SUBARRAYBEAMTARGET_OBJECT = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")

VALID_STNCONFIGURATION_JSON = """
{
    "station_id":1
}
"""

VALID_STNCONFIGURATION_OBJECT = StnConfiguration(1)

VALID_SUBARRAYBEAMCONFIGURATION_JSON = """
{
    "subarray_beam_id": 1,
    "station_ids": [1,2],
    "channels": [[1, 2]],
    "update_rate": 0.0,
    "antenna_weights": [1.0, 1.0, 1.0],
    "phase_centre": [0.0, 0.0],
    "target": """ + VALID_SUBARRAYBEAMTARGET_JSON + """
}
"""

VALID_SUBARRAYBEAMCONFIGURATION_OBJECT = SubarrayBeamConfiguration(
    subarray_beam_id=1,
    station_ids=[1, 2],
    channels=[[1, 2]],
    update_rate=0.0,
    target=VALID_SUBARRAYBEAMTARGET_OBJECT,
    antenna_weights=[1.0, 1.0, 1.0],
    phase_centre=[0.0, 0.0]
)

VALID_MCCSCONFIGURATION_JSON = """
{
    "stations": [
    """ + VALID_STNCONFIGURATION_JSON + """
    ],
    "subarray_beams": [
    """ + VALID_SUBARRAYBEAMCONFIGURATION_JSON + """
    ]
}
"""

VALID_MCCSCONFIGURATION_OBJECT = MCCSConfiguration(
    station_configs=[VALID_STNCONFIGURATION_OBJECT],
    subarray_beam_configs=[VALID_SUBARRAYBEAMCONFIGURATION_OBJECT]
)


@pytest.mark.parametrize('schema_cls,instance,expected', [
    (SubarrayBeamTargetSchema, VALID_SUBARRAYBEAMTARGET_OBJECT, VALID_SUBARRAYBEAMTARGET_JSON),
    (StnConfigurationSchema, VALID_STNCONFIGURATION_OBJECT, VALID_STNCONFIGURATION_JSON),
    (SubarrayBeamConfigurationSchema, VALID_SUBARRAYBEAMCONFIGURATION_OBJECT, VALID_SUBARRAYBEAMCONFIGURATION_JSON),
    (MCCSConfigurationSchema, VALID_MCCSCONFIGURATION_OBJECT, VALID_MCCSCONFIGURATION_JSON)
])
def test_marshal(schema_cls, instance, expected):
    """
    Verify that instances are marshaled to JSON correctly.
    """
    schema = schema_cls()
    marshaled = schema.dumps(instance)
    assert json_is_equal(expected, marshaled)

@pytest.mark.parametrize('schema_cls,json_str,expected', [
    (SubarrayBeamTargetSchema, VALID_SUBARRAYBEAMTARGET_JSON, VALID_SUBARRAYBEAMTARGET_OBJECT),
    (StnConfigurationSchema, VALID_STNCONFIGURATION_JSON, VALID_STNCONFIGURATION_OBJECT),
    (SubarrayBeamConfigurationSchema, VALID_SUBARRAYBEAMCONFIGURATION_JSON, VALID_SUBARRAYBEAMCONFIGURATION_OBJECT),
    (MCCSConfigurationSchema, VALID_MCCSCONFIGURATION_JSON, VALID_MCCSCONFIGURATION_OBJECT)
])
def test_unmarshal(schema_cls, json_str, expected):
    """
    Verify that instances are unmarshaled to instances correctly.
    """
    schema = schema_cls()
    unmarshaled = schema.loads(json_str)
    assert unmarshaled == expected

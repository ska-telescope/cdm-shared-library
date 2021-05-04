"""
Unit tests for ska.cdm.schemas.mccssubarray.assigned_resources module.
"""

import copy

import pytest

from ska.cdm.exceptions import JsonValidationError
from ska.cdm.messages.mccssubarray.configure import (
    ConfigureRequest,
    StationConfiguration,
    SubarrayBeamConfiguration
)
from ska.cdm.schemas.mccssubarray.configure import ConfigureRequestSchema
from ska.cdm.schemas.shared import ValidatingSchema
from ska.cdm.utils import json_is_equal

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-configure/1.0",
  "stations":[
    {
      "station_id": 1
    },
    {
      "station_id":2
    }
  ],
  "subarray_beams": [
    {
      "subarray_beam_id":1,
      "station_ids": [1, 2],
      "update_rate": 0.0,
      "channels": [
        [0,8,1,1],
        [8,8,2,1],
        [24,16,2,1]
      ],
      "sky_coordinates": [0.0, 180.0, 0.0, 45.0, 0.0],
      "antenna_weights": [1.0, 1.0, 1.0],
      "phase_centre": [0.0, 0.0]
    }
  ]
}
"""

INVALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-configure/1.0",
  "stations":[
    {
      "station_id": -1
    },
    {
      "station_id":2
    }
  ],
  "subarray_beams": [
    {
      "subarray_beam_id":1,
      "station_ids": [1, 2],
      "update_rate": 0.0,
      "channels": [
        [0,8,1,1],
        [8,8,2,1],
        [24,16,2,1]
      ],
      "sky_coordinates": [0.0, 180.0, 0.0, 45.0, 0.0],
      "antenna_weights": [1.0, 1.0, 1.0],
      "phase_centre": [0.0, 0.0]
    }
  ]
}
"""

VALID_OBJECT = ConfigureRequest(
    interface="https://schema.skatelescope.org/ska-low-mccs-configure/1.0",
    stations=[
        StationConfiguration(station_id=1),
        StationConfiguration(station_id=2)
    ],
    subarray_beams=[
        SubarrayBeamConfiguration(
            subarray_beam_id=1,
            station_ids=[1, 2],
            update_rate=0.0,
            channels=[
                [0, 8, 1, 1],
                [8, 8, 2, 1],
                [24, 16, 2, 1]
            ],
            sky_coordinates=[0.0, 180.0, 0.0, 45.0, 0.0],
            antenna_weights=[1.0, 1.0, 1.0],
            phase_centre=[0.0, 0.0]
        )
    ]
)


def test_marshal_configurerequest():
    """
    Verify that ConfigureRequest is marshalled to JSON correctly.
    """
    json_str = ConfigureRequestSchema().dumps(VALID_OBJECT)
    assert json_is_equal(json_str, VALID_JSON)


def test_unmarshal_configurerequest():
    """
    Verify that JSON can be unmarshalled back to an ConfigureRequest object.
    """
    unmarshalled = ConfigureRequestSchema().loads(VALID_JSON)
    assert unmarshalled == VALID_OBJECT


def test_deserialising_invalid_json_raises_exception_when_strict():
    """
    Verify that an exception is raised when invalid JSON is deserialised in
    strict mode.
    """
    schema = ConfigureRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.loads(INVALID_JSON)


def test_serialising_invalid_object_raises_exception_when_strict():
    """
    Verify that an exception is raised when an invalid object is serialised in
    strict mode.
    """
    o = copy.deepcopy(VALID_OBJECT)
    o.stations[0].station_id = -1

    schema = ConfigureRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.dumps(o)


def test_serialising_valid_object_does_not_raise_exception_when_strict():
    """
    Verify that an exception is not raised when a valid object is serialised
    in strict mode.
    """
    schema = ConfigureRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    _ = schema.dumps(VALID_OBJECT)

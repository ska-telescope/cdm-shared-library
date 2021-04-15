"""
Unit tests for ska.cdm.schemas.mccssubarray.assigned_resources module.
"""

from ska.cdm.messages.mccssubarray.configure import (
    ConfigureRequest,
    StationConfiguration,
    SubarrayBeamConfiguration
)
from ska.cdm.schemas.mccssubarray.configure import ConfigureRequestSchema
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

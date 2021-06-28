"""
Unit tests for ska_tmc_cdm.schemas.mccssubarray.assigned_resources module.
"""

import pytest

from ska_tmc_cdm.messages.mccssubarray.configure import (
    ConfigureRequest,
    StationConfiguration,
    SubarrayBeamConfiguration
)
from ska_tmc_cdm.schemas.mccssubarray.configure import ConfigureRequestSchema
from .. import utils

VALID_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-mccs-configure/2.0",
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
  "interface": "https://schema.skao.int/ska-low-mccs-configure/2.0",
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
    interface="https://schema.skao.int/ska-low-mccs-configure/2.0",
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


def modifier_fn(o):
    # function to make a valid ConfigureRequest invalid
    o.stations[0].station_id = -1


@pytest.mark.parametrize(
    'schema_cls,instance,modifier_fn,valid_json,invalid_json',
    [
        (ConfigureRequestSchema,
         VALID_OBJECT,
         modifier_fn,
         VALID_JSON,
         INVALID_JSON),
    ]
)
def test_assigned_resources_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that ConfigureRequestSchema marshals, unmarshals, and validates
    correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )

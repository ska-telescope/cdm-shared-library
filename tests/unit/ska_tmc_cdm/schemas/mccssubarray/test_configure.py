"""
Unit tests for ska_tmc_cdm.schemas.mccssubarray.assigned_resources module.
"""

import pytest

from ska_tmc_cdm.messages.mccssubarray.configure import (
    ConfigureRequest,
    StationConfiguration,
    SubarrayBeamAperatures,
    SubarrayBeamConfiguration,
    SubarrayBeamLogicalBands,
    SubarrayBeamSkyCoordinates,
)
from ska_tmc_cdm.schemas.mccssubarray.configure import ConfigureRequestSchema

from .. import utils

VALID_JSON = """
{
    "stations": [
      {
        "station_id": 1
      },
      {
        "station_id": 2
      }
    ],
    "subarray_beams": [
    {
        "subarray_beam_id": 1,
        "update_rate": 0.0,
        "logical_bands": [
          {
            "start_channel": 80,
            "number_of_channels": 16
          },
          {
            "start_channel": 384,
            "number_of_channels": 16
          }
        ],
        "apertures": [
          {
            "aperture_id": "AP001.01",
            "weighting_key_ref": "aperture2"
          },
          {
            "aperture_id": "AP001.02",
            "weighting_key_ref": "aperture3"
          },
          {
            "aperture_id": "AP002.01",
            "weighting_key_ref": "aperture2"
          },
          {
            "aperture_id": "AP002.02",
            "weighting_key_ref": "aperture3"
          },
          {
            "aperture_id": "AP003.01",
            "weighting_key_ref": "aperture1"
          }
        ],
        "sky_coordinates": {
          "timestamp": "2021-10-23T12:34:56.789Z",
          "reference_frame": "ICRS",
          "c1": 180.0,
          "c1_rate": 0.0,
          "c2": 45.0,
          "c2_rate": 0.0
        }
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
        "subarray_beam_id": 1,
        "update_rate": 0.0,
        "logical_bands": [
          {
            "start_channel": 80,
            "number_of_channels": 16
          },
          {
            "start_channel": 384,
            "number_of_channels": 16
          }
        ],
        "apertures": [
          {
            "aperture_id": "AP001.01",
            "weighting_key_ref": "aperture2"
          },
          {
            "aperture_id": "AP001.02",
            "weighting_key_ref": "aperture3"
          },
          {
            "aperture_id": "AP002.01",
            "weighting_key_ref": "aperture2"
          },
          {
            "aperture_id": "AP002.02",
            "weighting_key_ref": "aperture3"
          },
          {
            "aperture_id": "AP003.01",
            "weighting_key_ref": "aperture1"
          }
        ],
        "sky_coordinates": {
          "timestamp": "2021-10-23T12:34:56.789Z",
          "reference_frame": "ICRS",
          "c1": 180.0,
          "c1_rate": 0.0,
          "c2": 45.0,
          "c2_rate": 0.0
        }
      }
    ]
  }
"""

VALID_OBJECT = ConfigureRequest(
    interface="https://schema.skatelescope.org/ska-low-mccs-configure/1.0",
    stations=[StationConfiguration(station_id=1), StationConfiguration(station_id=2)],
    subarray_beams=[
        SubarrayBeamConfiguration(
            subarray_beam_id=1,
            station_ids=[1, 2],
            update_rate=0.0,
            channels=[[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 1]],
            antenna_weights=[1.0, 1.0, 1.0],
            phase_centre=[0.0, 0.0],
            logical_bands=[
                SubarrayBeamLogicalBands(start_channel=80, number_of_channels=16)
            ],
            apertures=[
                SubarrayBeamAperatures(
                    aperture_id="AP001.01", weighting_key_ref="aperture2"
                )
            ],
            sky_coordinates=SubarrayBeamSkyCoordinates(
                timestamp="2021-10-23T12:34:56.789Z",
                reference_frame="ICRS",
                c1=180.0,
                c1_rate=0.0,
                c2=45.0,
                c2_rate=0.0,
            ),
        )
    ],
)


def invalidate_configurerequest(o):
    # function to make a valid ConfigureRequest invalid
    o.stations[0].station_id = -1


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            ConfigureRequestSchema,
            VALID_OBJECT,
            invalidate_configurerequest,
            VALID_JSON,
            INVALID_JSON,
        ),
    ],
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

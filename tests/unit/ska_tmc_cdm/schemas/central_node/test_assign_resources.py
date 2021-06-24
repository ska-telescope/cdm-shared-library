"""
Unit tests for ska_tmc_cdm.schemas module.
"""

import pytest

from ska_tmc_cdm.messages.central_node.assign_resources import (
    AssignResourcesRequest,
    AssignResourcesResponse,
)
from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate
from ska_tmc_cdm.messages.central_node.sdp import (
    SDPConfiguration,
    ScanType,
    Channel,
    ProcessingBlockConfiguration,
    SDPWorkflow,
    PbDependency,
)
from ska_tmc_cdm.schemas.central_node.assign_resources import (
    AssignResourcesRequestSchema,
    AssignResourcesResponseSchema,
)
from ska_tmc_cdm.schemas.central_node.sdp import SDPConfigurationSchema
from .. import utils

VALID_SDP_JSON = """{
  "interface": "https://schema.skao.int/ska-sdp-assignresources/1.0",
  "eb_id": "eb-mvp01-20200325-00001",
  "max_length": 100.0,
  "scan_types": [
    {
      "scan_type_id": "science_A",
      "reference_frame": "ICRS",
      "ra": "02:42:40.771",
      "dec": "-00:00:47.84",
      "channels": [
        {
          "count": 744,
          "start": 0,
          "stride": 2,
          "freq_min": 0.35e9,
          "freq_max": 0.368e9,
          "link_map": [[0, 0], [200, 1], [744, 2], [944, 3]]
        },
        {
          "count": 744,
          "start": 2000,
          "stride": 1,
          "freq_min": 0.36e9,
          "freq_max": 0.368e9,
          "link_map": [[2000, 4], [2200, 5]]
        }
      ]
    },
    {
      "scan_type_id": "calibration_B",
      "reference_frame": "ICRS",
      "ra": "12:29:06.699",
      "dec": "02:03:08.598",
      "channels": [
        {
          "count": 744,
          "start": 0,
          "stride": 2,
          "freq_min": 0.35e9,
          "freq_max": 0.368e9,
          "link_map": [[0, 0], [200, 1], [744, 2], [944, 3]]
        },
        {
          "count": 744,
          "start": 2000,
          "stride": 1,
          "freq_min": 0.36e9,
          "freq_max": 0.368e9,
          "link_map": [[2000, 4], [2200, 5]]
        }
      ]
    }
  ],
  "processing_blocks": [
    {
      "pb_id": "pb-mvp01-20200325-00001",
      "workflow": {
        "kind": "realtime",
        "name": "vis_receive",
        "version": "0.1.0"
      },
      "parameters": {}
    },
    {
      "pb_id": "pb-mvp01-20200325-00002",
      "workflow": {
        "kind": "realtime",
        "name": "test_realtime",
        "version": "0.1.0"
      },
      "parameters": {}
    },
    {
      "pb_id": "pb-mvp01-20200325-00003",
      "workflow": {"kind": "batch", "name": "ical", "version": "0.1.0"},
      "parameters": {},
      "dependencies": [
        {"pb_id": "pb-mvp01-20200325-00001", "kind": ["visibilities"]}
      ]
    },
    {
      "pb_id": "pb-mvp01-20200325-00004",
      "workflow": {"kind": "batch", "name": "dpreb", "version": "0.1.0"},
      "parameters": {},
      "dependencies": [
        {"pb_id": "pb-mvp01-20200325-00003", "kind": ["calibration"]}
      ]
    }
  ]
}"""

VALID_SDP_OBJECT = SDPConfiguration(
    interface="https://schema.skao.int/ska-sdp-assignresources/1.0",
    sdp_id="eb-mvp01-20200325-00001",
    max_length=100.0,
    scan_types=[
        ScanType(
            "science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [
                Channel(
                    744, 0, 2, 0.35e9, 0.368e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
                ),
                Channel(
                    744, 2000, 1, 0.36e9, 0.368e9, [[2000, 4], [2200, 5]]
                )
            ]
        ),
        ScanType(
            "calibration_B", "ICRS", "12:29:06.699", "02:03:08.598", [
                Channel(
                    744, 0, 2, 0.35e9, 0.368e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
                ),
                Channel(
                    744, 2000, 1, 0.36e9, 0.368e9, [[2000, 4], [2200, 5]]
                )
            ]
        ),
    ],
    processing_blocks=[
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20200325-00001",
            workflow=SDPWorkflow("vis_receive", "realtime", "0.1.0"),
            parameters={}
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20200325-00002",
            workflow=SDPWorkflow("test_realtime", "realtime", "0.1.0"),
            parameters={}
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20200325-00003",
            workflow=SDPWorkflow("ical", "batch", "0.1.0"),
            parameters={},
            dependencies=[
                PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
            ]
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20200325-00004",
            workflow=SDPWorkflow("dpreb", "batch", "0.1.0"),
            parameters={},
            dependencies=[
                PbDependency("pb-mvp01-20200325-00003", ["calibration"])
            ])
    ]
)

VALID_MID_ASSIGNRESOURCESREQUEST_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/1.0",
  "transaction_id":"txn-mvp01-20200325-00004",
  "subarray_id": 1,
  "dish": {"receptor_ids": ["0001", "0002"]},
  "sdp": """ + VALID_SDP_JSON + """
}
"""

VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-assignresources/1.0",
    transaction_id="txn-mvp01-20200325-00004",
    subarray_id=1,
    dish_allocation=DishAllocation(
        receptor_ids=["0001", "0002"]
    ),
    sdp_config=VALID_SDP_OBJECT
)

VALID_LOW_ASSIGNRESOURCESREQUEST_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-tmc-assignresources/1.0",
  "transaction_id":"txn-mvp01-20200325-00004",
  "subarray_id": 1,
  "mccs": {
    "subarray_beam_ids": [1],
    "station_ids": [[1, 2]],
    "channel_blocks": [1, 2, 3, 4, 5]
  }
}
"""

VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-assignresources/1.0",
    transaction_id="txn-mvp01-20200325-00004",
    subarray_id=1,
    mccs=MCCSAllocate(
        subarray_beam_ids=[1],
        station_ids=[(1, 2)],
        channel_blocks=[1, 2, 3, 4, 5]
    )
)

INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON = """{
  "interface": "https://schema.skao.int/ska-low-tmc-assignresources/1.0",
  "subarray_id": 1,
  "mccs": {
    "subarray_beam_ids": [1, 2, 3],
    "station_ids": [[1, 2]],
    "channel_blocks": [1, 2, 3, 4, 5]
  }
}"""

VALID_MID_ASSIGNRESOURCESRESPONSE_JSON = """
{
    "dish": {"receptor_ids_success": ["0001", "0002"]}
}
"""

VALID_MID_ASSIGNRESOURCESRESPONSE_OBJECT = AssignResourcesResponse(
    dish_allocation=DishAllocation(["0001", "0002"])
)


def low_invalidator_fn(o: AssignResourcesRequest):
    # function to make a valid LOW AssignedResourcesRequest invalid
    o.mccs.subarray_beam_ids = [1, 2, 3]


@pytest.mark.xfail(reason="The Telescope Model library is not updated with ADR-35 hence, JSON schema validation will "
                          "be failed")
@pytest.mark.parametrize(
    'schema_cls,instance,modifier_fn,valid_json,invalid_json',
    [
        (AssignResourcesRequestSchema,
         VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
         low_invalidator_fn,
         VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
         INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON),
        (AssignResourcesRequestSchema,
         VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT,
         None,  # No validation for MID
         VALID_MID_ASSIGNRESOURCESREQUEST_JSON,
         None),  # No validation for MID
        (AssignResourcesResponseSchema,
         VALID_MID_ASSIGNRESOURCESRESPONSE_OBJECT,
         None,  # No validation for MID
         VALID_MID_ASSIGNRESOURCESRESPONSE_JSON,
         None),  # No validation for MID
        (SDPConfigurationSchema,
         VALID_SDP_OBJECT,
         None,  # No validation on SDP subschema
         VALID_SDP_JSON,
         None),  # No validation on SDP subschema
    ]
)
def test_releaseresources_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )
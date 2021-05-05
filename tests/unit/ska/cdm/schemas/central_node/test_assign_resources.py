"""
Unit tests for ska.cdm.schemas module.
"""
import copy

import pytest

from ska.cdm.exceptions import JsonValidationError
from ska.cdm.messages.central_node.assign_resources import (
    AssignResourcesRequest,
    AssignResourcesResponse,
)
from ska.cdm.messages.central_node.common import DishAllocation
from ska.cdm.messages.central_node.mccs import MCCSAllocate
from ska.cdm.messages.central_node.sdp import (
    SDPConfiguration,
    ScanType,
    Channel,
    ProcessingBlockConfiguration,
    SDPWorkflow,
    PbDependency,
)
from ska.cdm.schemas.central_node.assign_resources import (
    AssignResourcesRequestSchema,
    AssignResourcesResponseSchema,
)
from ska.cdm.schemas.central_node.sdp import SDPConfigurationSchema
from ska.cdm.schemas.shared import ValidatingSchema
from ska.cdm.utils import json_is_equal

VALID_MID_ASSIGNRESOURCESREQUEST_JSON = """
{
  "subarrayID": 1,
  "dish": {"receptorIDList": ["0001", "0002"]},
  "sdp": {
    "id": "sbi-mvp01-20200325-00001",
    "max_length": 100.0,
    "scan_types": [
      {
        "id": "science_A",
        "coordinate_system": "ICRS",
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
        "id": "calibration_B",
        "coordinate_system": "ICRS",
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
        "id": "pb-mvp01-20200325-00001",
        "workflow": {
          "type": "realtime",
          "id": "vis_receive",
          "version": "0.1.0"
        },
        "parameters": {}
      },
      {
        "id": "pb-mvp01-20200325-00002",
        "workflow": {
          "type": "realtime",
          "id": "test_realtime",
          "version": "0.1.0"
        },
        "parameters": {}
      },
      {
        "id": "pb-mvp01-20200325-00003",
        "workflow": {"type": "batch", "id": "ical", "version": "0.1.0"},
        "parameters": {},
        "dependencies": [
          {"pb_id": "pb-mvp01-20200325-00001", "type": ["visibilities"]}
        ]
      },
      {
        "id": "pb-mvp01-20200325-00004",
        "workflow": {"type": "batch", "id": "dpreb", "version": "0.1.0"},
        "parameters": {},
        "dependencies": [
          {"pb_id": "pb-mvp01-20200325-00003", "type": ["calibration"]}
        ]
      }
    ]
  }
}
"""

VALID_LOW_ASSIGNRESOURCESREQUEST_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-tmc-assignresources/1.0",
  "subarray_id": 1,
  "mccs": {
    "subarray_beam_ids": [1],
    "station_ids": [[1, 2]],
    "channel_blocks": [1, 2, 3, 4, 5]
  }
}
"""

VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skatelescope.org/ska-low-tmc-assignresources/1.0",
    subarray_id_low=1,
    mccs=MCCSAllocate(
        subarray_beam_ids=[1],
        station_ids=[(1, 2)],
        channel_blocks=[1, 2, 3, 4, 5]
    )
)

INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON = """{
  "interface": "https://schema.skatelescope.org/ska-low-tmc-assignresources/1.0",
  "subarray_id": 1,
  "mccs": {
    "subarray_beam_ids": [1, 2, 3],
    "station_ids": [[1, 2]],
    "channel_blocks": [1, 2, 3, 4, 5]
  }
}"""

VALID_SDP_CONFIG = """{
  "id": "sbi-mvp01-20200325-00001",
  "max_length": 100.0,
  "scan_types": [
    {
      "id": "science_A",
      "coordinate_system": "ICRS",
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
      "id": "calibration_B",
      "coordinate_system": "ICRS",
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
      "id": "pb-mvp01-20200325-00001",
      "workflow": {
        "type": "realtime",
        "id": "vis_receive",
        "version": "0.1.0"
      },
      "parameters": {}
    },
    {
      "id": "pb-mvp01-20200325-00002",
      "workflow": {
        "type": "realtime",
        "id": "test_realtime",
        "version": "0.1.0"
      },
      "parameters": {}
    },
    {
      "id": "pb-mvp01-20200325-00003",
      "workflow": {"type": "batch", "id": "ical", "version": "0.1.0"},
      "parameters": {},
      "dependencies": [
        {"pb_id": "pb-mvp01-20200325-00001", "type": ["visibilities"]}
      ]
    },
    {
      "id": "pb-mvp01-20200325-00004",
      "workflow": {"type": "batch", "id": "dpreb", "version": "0.1.0"},
      "parameters": {},
      "dependencies": [
        {"pb_id": "pb-mvp01-20200325-00003", "type": ["calibration"]}
      ]
    }
  ]
}"""

VALID_ASSIGN_RESOURCES_RESPONSE = """
{
    "dish": {"receptorIDList_success": ["0001", "0002"]}
}
"""


def sdp_config_for_test():  # pylint: disable=too-many-locals
    """
    Fixture which returns an SDPConfiguration object

    :return: SDPConfiguration
    """
    # scan_type
    channel_1 = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
    )
    channel_2 = Channel(744, 2000, 1, 0.36e9, 0.368e9, [[2000, 4], [2200, 5]])
    scan_type_a = ScanType(
        "science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [channel_1, channel_2]
    )
    scan_type_b = ScanType(
        "calibration_B", "ICRS", "12:29:06.699", "02:03:08.598", [channel_1, channel_2]
    )

    scan_types = [scan_type_a, scan_type_b]

    # PB workflow
    wf_a = SDPWorkflow("vis_receive", "realtime", "0.1.0")
    wf_b = SDPWorkflow("test_realtime", "realtime", "0.1.0")
    wf_c = SDPWorkflow("ical", "batch", "0.1.0")
    wf_d = SDPWorkflow("dpreb", "batch", "0.1.0")

    # PB Dependencies
    dep_a = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    dep_b = PbDependency("pb-mvp01-20200325-00003", ["calibration"])

    # SDP Processing blocks
    pb_a = ProcessingBlockConfiguration("pb-mvp01-20200325-00001", wf_a, {})
    pb_b = ProcessingBlockConfiguration("pb-mvp01-20200325-00002", wf_b, {})
    pb_c = ProcessingBlockConfiguration("pb-mvp01-20200325-00003", wf_c, {}, [dep_a])
    pb_d = ProcessingBlockConfiguration("pb-mvp01-20200325-00004", wf_d, {}, [dep_b])

    processing_blocks = [pb_a, pb_b, pb_c, pb_d]

    return SDPConfiguration(
        "sbi-mvp01-20200325-00001", 100.0, scan_types, processing_blocks
    )


def test_marshal_sdp_configuration():
    """
    Verify that SDPConfigurationSchema is marshalled to JSON correctly.
    """
    request = sdp_config_for_test()
    json_str = SDPConfigurationSchema().dumps(request)
    assert json_is_equal(json_str, VALID_SDP_CONFIG)


def test_unmarshall_assign_sdp_configuration():
    """
    Verify that JSON can be unmarshalled back to an SDPConfiguration
    object.
    """
    expected = sdp_config_for_test()
    request = SDPConfigurationSchema().loads(VALID_SDP_CONFIG)
    assert request == expected


def test_marshal_assign_resources_request_mid():
    """
    Verify that assign resource request for mid is marshalled
    to JSON correctly.
    """
    # SDP config
    sdp_config = sdp_config_for_test()
    # Dish allocation
    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    request = AssignResourcesRequest.from_dish(
        1, dish_allocation=dish_allocation, sdp_config=sdp_config,
    )
    json_str = AssignResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_MID_ASSIGNRESOURCESREQUEST_JSON)


def test_unmarshall_assign_resources_request_mid():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesRequest
    object for mid.
    """
    # SDP config
    sdp_config = sdp_config_for_test()
    dish = DishAllocation(receptor_ids=["0001", "0002"])
    request = AssignResourcesRequestSchema().loads(
        VALID_MID_ASSIGNRESOURCESREQUEST_JSON
    )
    expected = AssignResourcesRequest(subarray_id_mid=1,
                                      dish_allocation=dish,
                                      sdp_config=sdp_config)
    assert request == expected


def test_marshal_low_assignresourcesrequest():
    """
    Verify that assign resource request for low is marshalled
    to JSON correctly.
    """
    schema = AssignResourcesRequestSchema()
    marshaled = schema.dumps(VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT)
    assert json_is_equal(marshaled, VALID_LOW_ASSIGNRESOURCESREQUEST_JSON)


def test_unmarshall_low_assignresourcesrequest():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesRequest
    object for low.
    """
    schema = AssignResourcesRequestSchema()
    unmarshalled = schema.loads(VALID_LOW_ASSIGNRESOURCESREQUEST_JSON)
    assert unmarshalled == VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT


def test_marshall_assignresourcesresponse():
    """
    Verify that AssignResourcesResponse is marshalled to JSON correctly.
    """
    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)
    json_str = AssignResourcesResponseSchema().dumps(response)
    assert json_is_equal(json_str, VALID_ASSIGN_RESOURCES_RESPONSE)


def test_unmarshall_assignresourcesresponse():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesResponse
    object.
    """
    response = AssignResourcesResponseSchema().loads(VALID_ASSIGN_RESOURCES_RESPONSE)
    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    expected = AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response == expected


def test_deserialising_invalid_low_json_raises_exception_when_strict():
    """
    Verify that an exception is raised when invalid JSON is deserialised in
    strict mode.
    """
    schema = AssignResourcesRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.loads(INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON)


def test_serialising_invalid_low_allocation_raises_exception_when_strict():
    """
    Verify that an exception is raised when an invalid object is serialised in
    strict mode.
    """
    o = copy.deepcopy(VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT)
    o.mccs.subarray_beam_ids = [1, 2, 3]

    schema = AssignResourcesRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.dumps(o)


def test_serialising_valid_low_allocation_does_not_raise_exception_when_strict():
    """
    Verify that an exception is not raised when a valid object is serialised
    in strict mode.
    """
    schema = AssignResourcesRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    _ = schema.dumps(VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT)

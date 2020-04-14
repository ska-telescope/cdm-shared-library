"""
Unit tests for ska.cdm.schemas module.
"""

import pytest

from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest, \
    AssignResourcesResponse, DishAllocation, SDPConfiguration, ScanType, SubBand, \
    ProcessingBlockConfiguration, SDPWorkflow, PbDependency
from ska.cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska.cdm.schemas.central_node import SDPConfigurationSchema, AssignResourcesRequestSchema, \
    AssignResourcesResponseSchema, ReleaseResourcesRequestSchema
from .utils import json_is_equal


VALID_ASSIGN_RESOURCES_REQUEST = """
{
  "subarrayID": 1,
  "dish": {
    "receptorIDList": ["0001", "0002"]
  },
  "sdp": {
  "id": "sbi-mvp01-20200325-00001",
  "max_length": 100.0,
  "scan_types": [
    {
      "id": "science_A",
      "coordinate_system": "ICRS", "ra": "02:42:40.771", "dec": "-00:00:47.84",
      "subbands": [{
         "freq_min": 0.35e9, "freq_max": 1.05e9, "nchan": 372,
         "input_link_map": [[1,0], [101,1]]
      }]
    },
    {
      "id": "calibration_B",
      "coordinate_system": "ICRS", "ra": "12:29:06.699", "dec": "02:03:08.598",
      "subbands": [{
        "freq_min": 0.35e9, "freq_max": 1.05e9, "nchan": 372,
        "input_link_map": [[1,0], [101,1]]
      }]
    }
  ],
  "processing_blocks": [
    {
      "id": "pb-mvp01-20200325-00001",
      "workflow": {"type": "realtime", "id": "vis_receive", "version": "0.1.0"},
      "parameters": {}
    },
    {
      "id": "pb-mvp01-20200325-00002",
      "workflow": {"type": "realtime", "id": "test_realtime", "version": "0.1.0"},
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
}"""

VALID_SDP_CONFIG = """
{
  "id": "sbi-mvp01-20200325-00001",
  "max_length": 100.0,
  "scan_types": [
    {
      "id": "science_A",
      "coordinate_system": "ICRS", "ra": "02:42:40.771", "dec": "-00:00:47.84",
      "subbands": [{
         "freq_min": 0.35e9, "freq_max": 1.05e9, "nchan": 372,
         "input_link_map": [[1,0], [101,1]]
      }]
    },
    {
      "id": "calibration_B",
      "coordinate_system": "ICRS", "ra": "12:29:06.699", "dec": "02:03:08.598",
      "subbands": [{
        "freq_min": 0.35e9, "freq_max": 1.05e9, "nchan": 372,
        "input_link_map": [[1,0], [101,1]]
      }]
    }
  ],
  "processing_blocks": [
    {
      "id": "pb-mvp01-20200325-00001",
      "workflow": {"type": "realtime", "id": "vis_receive", "version": "0.1.0"},
      "parameters": {}
    },
    {
      "id": "pb-mvp01-20200325-00002",
      "workflow": {"type": "realtime", "id": "test_realtime", "version": "0.1.0"},
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

VALID_ASSIGN_RESOURCES_RESPONSE = '{"dish": {"receptorIDList_success": ["0001", "0002"]}}'
VALID_RELEASE_RESOURCES_REQUEST = '{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}'
VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST = '{"subarrayID": 1, "releaseALL": true}'


def sdp_config_for_test():  # pylint: disable=too-many-locals
    """
    Fixture which returns an SDPConfiguration object
    """
    # scan_type
    sub_band_a = SubBand(0.35e9, 1.05e9, 372, [[1, 0], [101, 1]])
    sub_band_b = SubBand(0.35e9, 1.05e9, 372, [[1, 0], [101, 1]])
    scan_type_a = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [sub_band_a])
    scan_type_b = ScanType("calibration_B", "ICRS", "12:29:06.699", "02:03:08.598", [sub_band_b])

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

    return SDPConfiguration("sbi-mvp01-20200325-00001", 100.0, scan_types, processing_blocks)


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


def test_marshal_assign_resources_request():
    """
    Verify that AssignResourcesRequest is marshalled to JSON correctly.
    """
    # SDP config
    sdp_config = sdp_config_for_test()
    # Dish allocation
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])

    request = AssignResourcesRequest(1, dish_allocation=dish_allocation, sdp_config=sdp_config)
    json_str = AssignResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_ASSIGN_RESOURCES_REQUEST)


def test_unmarshall_assign_resources_request():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesRequest
    object.
    """
    sdp_config = sdp_config_for_test()

    request = AssignResourcesRequestSchema().loads(VALID_ASSIGN_RESOURCES_REQUEST)
    expected = AssignResourcesRequest(1, DishAllocation(
        receptor_ids=['0001', '0002']), sdp_config=sdp_config)
    assert request == expected


def test_marshall_assign_resources_response():
    """
    Verify that AssignResourcesResponse is marshalled to JSON correctly.
    """
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)
    json_str = AssignResourcesResponseSchema().dumps(response)
    assert json_is_equal(json_str, VALID_ASSIGN_RESOURCES_RESPONSE)


def test_unmarshall_assign_resources_response():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesResponse
    object.
    """
    response = AssignResourcesResponseSchema().loads(VALID_ASSIGN_RESOURCES_RESPONSE)
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    expected = AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response == expected


def test_marshall_release_resources():
    """
    Verify that ReleaseResourcesRequest is marshalled to JSON correctly.
    """
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    request = ReleaseResourcesRequest(1, dish_allocation=dish_allocation)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_REQUEST)


def test_marshall_release_resources_release_all():
    """
    Verify that ReleaseResourcesRequest with release_all set is marshalled to
    JSON correctly.
    """
    request = ReleaseResourcesRequest(1, release_all=True)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_release_resources_ignores_resources_when_release_all_is_specified():
    """
    Verify that other resource statements are excluded when release_all is set
    to True.
    """
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    request = ReleaseResourcesRequest(1, release_all=True,
                                      dish_allocation=dish_allocation)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_unmarshall_release_resources():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object.
    """
    schema = ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_RELEASE_RESOURCES_REQUEST)
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    expected = ReleaseResourcesRequest(1, dish_allocation=dish_allocation)
    assert request == expected


def test_unmarshall_release_resources_with_release_all_set():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object when release_all is set.
    """
    schema = ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)
    expected = ReleaseResourcesRequest(1, release_all=True)
    assert request == expected

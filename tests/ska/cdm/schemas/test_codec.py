"""
Unit tests for the ska.cdm.schemas.codec module.
"""
import os.path
import unittest.mock as mock
import pytest
from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska.cdm.messages.central_node.common import DishAllocation
from ska.cdm.messages.central_node.mccs import MCCSAllocate
from ska.cdm.messages.subarray_node.configure import ConfigureRequest
from ska.cdm.messages.subarray_node.configure.csp import (
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration,
    CBFConfiguration,
    CommonConfiguration,
)
from ska.cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    ReceiverBand,
)
import ska.cdm.jsonschema.json_schema as json_schema
from ska.cdm.schemas import CODEC
from ska.cdm.utils import json_is_equal
from ska.cdm.exceptions import JsonValidationError
from .central_node.test_central_node import (
    VALID_ASSIGN_RESOURCES_REQUEST,
    VALID_MCCS_ALLOCATE_RESOURCES_REQUEST,
    sdp_config_for_test,
)


def test_codec_loads():
    """
    Verify that the codec unmarshalls objects correctly.
    """
    sdp_config = sdp_config_for_test()
    unmarshalled = CODEC.loads(AssignResourcesRequest, VALID_ASSIGN_RESOURCES_REQUEST)
    expected = AssignResourcesRequest.from_dish(
        1, DishAllocation(receptor_ids=["0001", "0002"]), sdp_config=sdp_config,
    )
    assert expected == unmarshalled


def test_codec_loads_mccs_only():
    """
    Verify that the codec unmarshalls objects correctly.
    """
    mccs_allocate = MCCSAllocate(
        1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    unmarshalled = CODEC.loads(
        AssignResourcesRequest, VALID_MCCS_ALLOCATE_RESOURCES_REQUEST
    )
    expected = AssignResourcesRequest.from_mccs(mccs_allocate=mccs_allocate)
    assert expected == unmarshalled


def test_codec_dumps():
    """
    Verify that the codec marshalls dish & sdp objects to JSON.
    """
    sdp_config = sdp_config_for_test()
    expected = VALID_ASSIGN_RESOURCES_REQUEST
    obj = AssignResourcesRequest(
        1, DishAllocation(receptor_ids=["0001", "0002"]), sdp_config=sdp_config
    )

    marshalled = CODEC.dumps(obj)
    assert json_is_equal(marshalled, expected)


def test_codec_dumps_mccs():
    """
    Verify that the codec marshalls mccs objects to JSON.
    """
    mccs_allocate = MCCSAllocate(
        1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    expected = VALID_MCCS_ALLOCATE_RESOURCES_REQUEST
    obj = AssignResourcesRequest.from_mccs(mccs_allocate=mccs_allocate)

    marshalled = CODEC.dumps(obj)
    assert json_is_equal(marshalled, expected)


def test_read_a_file_from_disk():
    """
    Test for loading a configure request from a JSON file
    """
    cwd, _ = os.path.split(__file__)
    test_data = os.path.join(cwd, "testfile_sample_configure.json")
    result = CODEC.load_from_file(ConfigureRequest, test_data)
    dish_config = DishConfiguration(ReceiverBand.BAND_1)
    assert result.dish == dish_config

    test_new_json_data = os.path.join(cwd, "testfile_sample_configure_ADR_18.json")
    result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data)
    dish_config = DishConfiguration(ReceiverBand.BAND_1)
    assert result_data.dish == dish_config


VALID_CSP_SCHEMA = """{
    "interface": "https://schema.skatelescope.org/ska-csp-configure/1.0",
    "subarray": {
      "subarrayName": "science period 23"
    },
    "common": {
      "id": "sbi-mvp01-20200325-00001-science_A",
      "frequencyBand": "1",
      "subarrayID": 1
    },
    "cbf": {
      "fsp": [
        {
          "fspID": 1,
          "functionMode": "CORR",
          "frequencySliceID": 1,
          "integrationTime": 1400,
          "outputLinkMap": [[0,0], [200,1]],
          "corrBandwidth": 0,
          "channelAveragingMap": [[0, 2], [744, 0]],
          "fspChannelOffset": 0
        },
        {
          "fspID": 2,
          "functionMode": "CORR",
          "frequencySliceID": 2,
          "integrationTime": 1400,
          "corrBandwidth": 1,
          "outputLinkMap": [[0,4], [200,5]],
          "channelAveragingMap": [[0, 2], [744, 0]],
          "fspChannelOffset": 744,
          "zoomWindowTuning": 4700000
        }
      ]
    }
  }
   """

INVALID_CSP_SCHEMA = """{
    "interface": "https://schema.skatelescope.org/ska-csp-configure/3.0",
    "subarray": {
      "subarrayName": "science period 23"
    },
    "common": {
      "id": "sbi-mvp01-20200325-00001-science_A",
      "frequencyBand": "1",
      "subarrayID": 1
    }
  }
"""


def csp_config_for_test():
    """
    Fixture which returns an CSPConfiguration object

    :return: CSPConfiguration
    """

    csp_id = "sbi-mvp01-20200325-00001-science_A"
    # TODO refactor this as a builder, consolidate duplicate code
    fsp_config_1 = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_averaging_map=[(0, 2), (744, 0)],
        fsp_channel_offset=0,
        output_link_map=[(0, 0), (200, 1)]
    )
    fsp_config_2 = FSPConfiguration(
        2,
        FSPFunctionMode.CORR,
        2,
        1400,
        1,
        channel_averaging_map=[(0, 2), (744, 0)],
        fsp_channel_offset=744,
        output_link_map=[(0, 4), (200, 5)],
        zoom_window_tuning=4700000,
    )

    cbf_config = CBFConfiguration([fsp_config_1, fsp_config_2])
    csp_subarray_config = SubarrayConfiguration('science period 23')
    csp_common_config = CommonConfiguration(csp_id, ReceiverBand.BAND_1, 1)
    csp_config = CSPConfiguration(
        interface_url="https://schema.skatelescope.org/ska-csp-configure/1.0",
        subarray_config=csp_subarray_config,
        common_config=csp_common_config,
        cbf_config=cbf_config
    )
    return csp_config


def test_codec_loads_raises_exception_on_invalid_schema():
    """
     Verify that codec loads() with invalid schema raise exception
    """
    with pytest.raises(JsonValidationError):
        CODEC.loads(CSPConfiguration, INVALID_CSP_SCHEMA)


def test_codec_dumps_raises_exception_on_invalid_schema():
    """
     Verify that codec dumps() with invalid schema raise exception
    """
    csp_config = csp_config_for_test()
    csp_config.interface_url = 'http://schema.skatelescope.org/ska-csp-configure/3.0'
    with pytest.raises(JsonValidationError):
        CODEC.dumps(csp_config)


def test_codec_dumps_with_schema_validation_for_csp():
    """
    Verify that the codec marshalls csp objects to JSON with schema
    validation.
    """
    expected = VALID_CSP_SCHEMA
    csp_config = csp_config_for_test()
    marshalled = CODEC.dumps(csp_config)
    assert json_is_equal(marshalled, expected)


def test_codec_loads_with_schema_validation_for_csp():
    """
    Verify that the codec unmarshalls objects correctly with schema
    validation.
    """
    csp_config = csp_config_for_test()
    unmarshalled = CODEC.loads(CSPConfiguration, VALID_CSP_SCHEMA)
    assert csp_config == unmarshalled


@mock.patch.object(json_schema.JsonSchema, 'validate_schema')
def test_codec_loads_from_file_with_schema_validation(mock_fn):
    """
    Verify that the codec unmarshalls objects correctly with schema
    validation and Test it with loading a valid ADR18-configure request
    from a JSON file
    """
    csp_config = csp_config_for_test()
    cwd, _ = os.path.split(__file__)
    test_new_json_data = os.path.join(cwd, "testfile_sample_configure_ADR_18.json")
    result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data)
    assert result_data.csp == csp_config
    assert mock_fn.call_count == 1
    mock_fn.assert_called_once()


@mock.patch.object(json_schema.JsonSchema, 'validate_schema')
def test_codec_loads_from_file_without_schema_validation(mock_fn):
    """
    Verify that the codec unmarshalls objects correctly without schema
    validation and Test it with loading a valid ADR18-configure request
    from a JSON file
    """
    csp_config = csp_config_for_test()
    cwd, _ = os.path.split(__file__)
    test_new_json_data = os.path.join(cwd, "testfile_sample_configure_ADR_18.json")
    result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data, False)
    assert result_data.csp == csp_config
    assert mock_fn.call_count == 0
    mock_fn.assert_not_called()


# @mock.patch.object(json_schema.JsonSchema, 'validate_schema')
# def test_loads_from_file_with_invalid_schema_and_validation_set_to_true(mock_fn):
#     """
#     Verify that the codec unmarshalls objects correctly with schema
#     validation and Test it with loading a invalid ADR18-configure request
#     from a JSON file
#     """
#
#     csp_config = csp_config_for_test()
#     cwd, _ = os.path.split(__file__)
#     test_new_json_data = os.path.join(cwd, "testfile_invalid_configure_ADR_18.json")
#     with pytest.raises(JsonValidationError):
#         CODEC.load_from_file(ConfigureRequest, test_new_json_data)
#     assert mock_fn.call_count == 1
#     mock_fn.assert_called_once()


@mock.patch.object(json_schema.JsonSchema, 'validate_schema')
def test_loads_from_file_with_invalid_schema_and_validation_set_to_false(mock_fn):
    """
    Verify that the codec unmarshalls objects correctly without schema
    validation and Test it with loading a invalid ADR18-configure request
    from a JSON file
    """
    csp_config = csp_config_for_test()
    cwd, _ = os.path.split(__file__)
    test_new_json_data = os.path.join(cwd, "testfile_invalid_configure_ADR_18.json")
    result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data, False)
    assert result_data.csp.subarray_config is None
    assert mock_fn.call_count == 0
    mock_fn.assert_not_called()


@mock.patch.object(json_schema.JsonSchema, 'validate_schema')
def test_codec_loads_from_file_with_schema_validation_for_old_json(mock_fn):
    """
    Verify that the schema validation does not apply even it is set to true
    for pre ADR-18 JSON schema
    """
    cwd, _ = os.path.split(__file__)
    test_new_json_data = os.path.join(cwd, "testfile_sample_configure.json")
    result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data)
    assert mock_fn.call_count == 0
    mock_fn.assert_not_called()


@mock.patch.object(json_schema.JsonSchema, 'validate_schema')
def test_codec_loads_from_file_without_schema_validation_for_old_json(mock_fn):
    """
    Verify that the schema validation does not apply when it is set to false
    for pre ADR-18 JSON schema
    """
    cwd, _ = os.path.split(__file__)
    test_new_json_data = os.path.join(cwd, "testfile_sample_configure.json")
    result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data, False)
    assert mock_fn.call_count == 0
    mock_fn.assert_not_called()

"""
Unit tests for the ska_tmc_cdm.schemas.codec module.
"""
import os.path
import unittest.mock as mock

import pytest

from ska_tmc_cdm.exceptions import JsonValidationError
from ska_tmc_cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate
from ska_tmc_cdm.messages.subarray_node.configure import ConfigureRequest
from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    ReceiverBand,
)
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration,
    CBFConfiguration,
    CommonConfiguration,
)
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.utils import json_is_equal

import ska_tmc_cdm

from .central_node.test_assign_resources import (
    VALID_MID_ASSIGNRESOURCESREQUEST_JSON,
    VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
    VALID_SDP_OBJECT,
)

VALID_CONFIGURE_REQUEST = """
{
  "pointing": {
    "target": {
      "reference_frame": "ICRS",
      "target_name": "M51",
      "ra": "13:29:52.698",
      "dec": "+47:11:42.93"
    }
  },
  "dish": {
    "receiver_band": "1"
  },
  "csp": {
    "interface": "https://schema.skatelescope.org/ska-csp-configure/1.0",
    "subarray": {
      "subarray_name": "science period 23"
    },
    "common": {
      "config_id": "sbi-mvp01-20200325-00001-science_A",
      "frequency_band": "1",
      "subarray_id": 1
    },
    "cbf": {
      "fsp": [
        {
          "fsp_id": 1,
          "function_mode": "CORR",
          "frequency_slice_id": 1,
          "integration_factor": 10,
          "output_link_map": [[0,0], [200,1]],
          "zoom_factor": 0,
          "channel_averaging_map": [[0, 2], [744, 0]],
          "channel_offset": 0
        },
        {
          "fsp_id": 2,
          "function_mode": "CORR",
          "frequency_slice_id": 2,
          "integration_factor": 10,
          "zoom_factor": 1,
          "output_link_map": [[0,4], [200,5]],
          "channel_averaging_map": [[0, 2], [744, 0]],
          "channel_offset": 744,
          "zoom_window_tuning": 4700000
        }
      ]
    }
  },
  "sdp": {
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": 10.0
  }
}
"""

INVALID_CONFIGURE_REQUEST = """
{
  "pointing": {
    "target": {
      "reference_frame": "ICRS",
      "target_name": "M51",
      "ra": "13:29:52.698",
      "dec": "+47:11:42.93"
    }
  },
  "dish": {
    "receiver_band": "1"
  },
  "csp": {
    "interface": "https://schema.skatelescope.org/ska-csp-configure/1.0",
    "cbf": {
      "fsp": [
        {
          "fsp_id": 1,
          "function_mode": "CORR",
          "frequency_slice_id": 1,
          "integration_factor": 10,
          "output_link_map": [[0,0], [200,1]],
          "zoom_factor": 0,
          "channel_averaging_map": [[0, 2], [744, 0]],
          "channel_offset": 0
        },
        {
          "fsp_id": 2,
          "function_mode": "CORR",
          "frequency_slice_id": 2,
          "integration_factor": 10,
          "zoom_factor": 1,
          "output_link_map": [[0,4], [200,5]],
          "channel_averaging_map": [[0, 2], [744, 0]],
          "channel_offset": 744,
          "zoom_window_tuning": 4700000
        }
      ]
    }
  },
  "sdp": {
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": 10.0
  }
}
"""

VALID_CSP_SCHEMA = """{
    "interface": "https://schema.skatelescope.org/ska-csp-configure/1.0",
    "subarray": {
      "subarray_name": "science period 23"
    },
    "common": {
      "config_id": "sbi-mvp01-20200325-00001-science_A",
      "frequency_band": "1",
      "subarray_id": 1
    },
    "cbf": {
      "fsp": [
        {
          "fsp_id": 1,
          "function_mode": "CORR",
          "frequency_slice_id": 1,
          "integration_factor": 10,
          "output_link_map": [[0,0], [200,1]],
          "zoom_factor": 0,
          "channel_averaging_map": [[0, 2], [744, 0]],
          "channel_offset": 0
        },
        {
          "fsp_id": 2,
          "function_mode": "CORR",
          "frequency_slice_id": 2,
          "integration_factor": 10,
          "zoom_factor": 1,
          "output_link_map": [[0,4], [200,5]],
          "channel_averaging_map": [[0, 2], [744, 0]],
          "channel_offset": 744,
          "zoom_window_tuning": 4700000
        }
      ]
    }
  }
"""

INVALID_CSP_SCHEMA = """{
    "interface": "https://schema.skatelescope.org/ska-csp-configure/9999999.0",
    "subarray": {
      "subarray_name": "science period 23"
    },
    "common": {
      "config_id": "sbi-mvp01-20200325-00001-science_A",
      "frequency_band": "1",
      "subarray_id": 1
    }
  }
"""


# TODO remove xfail before merging AT2-855
@pytest.mark.xfail(reason="The Telescope Model library is not updated with "
                          "ADR-35 hence JSON schema validation will fail")
def test_codec_loads():
    """
    Verify that the codec unmarshalls objects correctly.
    """
    sdp_config = VALID_SDP_OBJECT
    unmarshalled = CODEC.loads(AssignResourcesRequest,
                               VALID_MID_ASSIGNRESOURCESREQUEST_JSON
                               )
    expected = AssignResourcesRequest.from_dish(
        subarray_id=1,
        dish_allocation=DishAllocation(receptor_ids=["0001", "0002"]),
        sdp_config=sdp_config,
        interface='https://schema.skao.int/ska-tmc-assignresources/2.0',
        transaction_id='txn-mvp01-20200325-00004'
    )
    assert expected == unmarshalled


def test_codec_loads_mccs_only():
    """
    Verify that the codec unmarshalls objects correctly.
    """
    interface = 'https://schema.skao.int/ska-low-tmc-assignresources/2.0'
    mccs = MCCSAllocate(
        subarray_beam_ids=[1],
        station_ids=[(1, 2)],
        channel_blocks=[1, 2, 3, 4, 5]
    )
    expected = AssignResourcesRequest.from_mccs(
        interface=interface,
        subarray_id=1,
        mccs=mccs,
        transaction_id="txn-mvp01-20200325-00004"
    )

    assert expected == VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT


# TODO remove xfail before merging AT2-855
@pytest.mark.xfail(reason="The Telescope Model library is not updated with "
                          "ADR-35 hence JSON schema validation will fail")
def test_codec_dumps():
    """
    Verify that the codec marshalls dish & sdp objects to JSON.
    """
    sdp_config = VALID_SDP_OBJECT
    expected = VALID_MID_ASSIGNRESOURCESREQUEST_JSON
    obj = AssignResourcesRequest(
        subarray_id=1,
        dish_allocation=DishAllocation(receptor_ids=["0001", "0002"]),
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00004"
    )

    marshalled = CODEC.dumps(obj)
    assert json_is_equal(marshalled, expected)


def test_read_a_file_from_disk():
    """
    Test for loading a configure request from a JSON file
    """
    cwd, _ = os.path.split(__file__)
    test_new_json_data = os.path.join(cwd, "testfile_sample_configure.json")
    result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data)
    dish_config = DishConfiguration(ReceiverBand.BAND_1)
    assert result_data.dish == dish_config


def csp_config_for_test():
    """
    Fixture which returns an CSPConfiguration object

    :return: CSPConfiguration
    """

    config_id = "sbi-mvp01-20200325-00001-science_A"
    # TODO refactor this as a builder, consolidate duplicate code
    fsp_config_1 = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        10,
        0,
        channel_averaging_map=[(0, 2), (744, 0)],
        channel_offset=0,
        output_link_map=[(0, 0), (200, 1)]
    )
    fsp_config_2 = FSPConfiguration(
        2,
        FSPFunctionMode.CORR,
        2,
        10,
        1,
        channel_averaging_map=[(0, 2), (744, 0)],
        channel_offset=744,
        output_link_map=[(0, 4), (200, 5)],
        zoom_window_tuning=4700000,
    )

    cbf_config = CBFConfiguration([fsp_config_1, fsp_config_2])
    csp_subarray_config = SubarrayConfiguration('science period 23')
    csp_common_config = CommonConfiguration(config_id, ReceiverBand.BAND_1, 1)
    csp_config = CSPConfiguration(
        interface="https://schema.skatelescope.org/ska-csp-configure/1.0",
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
    csp_config.interface = 'http://schema.skatelescope.org/ska-csp-configure/3.0'
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


@mock.patch("ska_tmc_cdm.jsonschema.json_schema.schema.validate")
def test_codec_loads_from_file_with_schema_validation(mock_fn):
    """
    Verify that the codec unmarshalls objects correctly with schema
    validation and Test it with loading a valid ADR18-configure request
    from a JSON file
    """
    csp_config = csp_config_for_test()
    cwd, _ = os.path.split(__file__)
    test_new_json_data = os.path.join(cwd, "testfile_sample_configure.json")
    result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data)
    assert result_data.csp == csp_config
    assert mock_fn.call_count == 1
    mock_fn.assert_called_once()


@mock.patch("ska_tmc_cdm.jsonschema.json_schema.schema.validate")
def test_codec_loads_from_file_without_schema_validation(mock_fn):
    """
    Verify that the codec unmarshalls objects correctly without schema
    validation and Test it with loading a valid ADR18-configure request
    from a JSON file
    """
    csp_config = csp_config_for_test()
    cwd, _ = os.path.split(__file__)
    test_new_json_data = os.path.join(cwd, "testfile_sample_configure.json")
    result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data, validate=False)
    assert result_data.csp == csp_config
    assert mock_fn.call_count == 0
    mock_fn.assert_not_called()


# TODO remove xfail before merging AT2-855
@pytest.mark.xfail(reason="The Telescope Model library is not updated with "
                          "ADR-35 hence JSON schema validation will fail")
def test_loads_from_file_with_invalid_schema_and_validation_set_to_true():
    """
    Verify that the codec unmarshalls objects correctly with schema
    validation and Test it with loading a invalid ADR18-configure request
    from a JSON file
    """
    cwd, _ = os.path.split(__file__)
    test_new_json_data = os.path.join(cwd, "testfile_invalid_configure.json")
    with pytest.raises(JsonValidationError):
        CODEC.load_from_file(ConfigureRequest, test_new_json_data)


@mock.patch("ska_tmc_cdm.jsonschema.json_schema.schema.validate")
def test_loads_from_file_with_invalid_schema_and_validation_set_to_false(mock_fn):
    """
    Verify that the codec unmarshalls objects correctly without schema
    validation and Test it with loading a invalid ADR18-configure request
    from a JSON file
    """
    cwd, _ = os.path.split(__file__)
    test_new_json_data = os.path.join(cwd, "testfile_invalid_configure.json")
    result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data, False)
    assert result_data.csp.subarray_config is None
    assert mock_fn.call_count == 0
    mock_fn.assert_not_called()


# TODO remove xfail before merging AT2-855
@pytest.mark.xfail(reason="The Telescope Model library is not updated with "
                          "ADR-35 hence JSON schema validation will fail")
def test_configure_request_raises_exception_when_loads_invalid_csp_schema():
    """
     Verify that codec loads() with invalid schema raise exception
    """
    with pytest.raises(JsonValidationError):
        CODEC.loads(ConfigureRequest, INVALID_CONFIGURE_REQUEST)


def test_configure_request_raises_exception_on_invalid_csp_object():
    """
     Verify that codec dumps() with invalid schema raise exception
    """
    configure_request = CODEC.loads(ConfigureRequest, VALID_CONFIGURE_REQUEST)
    configure_request.csp.interface = \
        'http://schema.skatelescope.org/ska-csp-configure/3.0'

    with pytest.raises(JsonValidationError):
        CODEC.dumps(configure_request, strictness=2)


@pytest.mark.parametrize('message_cls', [
    ska_tmc_cdm.messages.central_node.assign_resources.AssignResourcesRequest,
    ska_tmc_cdm.messages.central_node.assign_resources.AssignResourcesResponse,
    ska_tmc_cdm.messages.central_node.release_resources.ReleaseResourcesRequest,
    ska_tmc_cdm.messages.subarray_node.configure.ConfigureRequest,
    ska_tmc_cdm.messages.subarray_node.scan.ScanRequest,
    ska_tmc_cdm.messages.subarray_node.assigned_resources.AssignedResources,
    ska_tmc_cdm.messages.mccscontroller.allocate.AllocateRequest,
    ska_tmc_cdm.messages.mccscontroller.releaseresources.ReleaseResourcesRequest,
    ska_tmc_cdm.messages.mccssubarray.configure.ConfigureRequest,
    ska_tmc_cdm.messages.mccssubarray.scan.ScanRequest,
    ska_tmc_cdm.messages.mccssubarray.assigned_resources.AssignedResources
])
def test_schema_registration(message_cls):
    """
    Verify that a schema is registered with the MarshmallowCodec.
    """
    assert message_cls in CODEC._schema

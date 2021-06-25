"""
Unit tests for the ska_tmc_cdm.jsonschema.json_schema module.
"""
from unittest import mock
import pytest
from ska_tmc_cdm.jsonschema.json_schema import JsonSchema

VALID_JSON = {"interface": "https://schema.skatelescope.org/ska-csp-configure/1.0",
              "subarray": {"subarray_name": "science period 23"},
              "common": {"config_id": "sbi-mvp01-20200325-00001-science_A",
                         "frequencyBand": "1",
                         "subarray_id": 1},
              "cbf": {"fsp": [{"fsp_id": 1, "function_mode": "CORR",
                               "frequency_slice_id": 1,
                               "integration_factor": 10,
                               "zoom_factor": 0,
                               "channel_averaging_map": [[0, 2], [744, 0]],
                               "channel_offset": 0,
                               "output_link_map": [[0, 0], [200, 1]]},
                              {"fsp_id": 2, "function_mode": "CORR",
                               "frequency_slice_id": 2,
                               "integration_factor": 10,
                               "zoom_factor": 0,
                               "channel_averaging_map": [[0, 2], [744, 0]],
                               "channel_offset": 744,
                               "output_link_map": [[0, 4], [200, 5]]}],
                      "vlbi": {}},
              "pss": {}}
INVALID_JSON = {"interface": "https://schema.skatelescope.org/ska-csp-configure/5.0",
                "subarray": {"subarray_name": "science period 23"},
                "common": {"config_id": "sbi-mvp01-20200325-00001-science_A",
                           "frequencyBand": "1",
                           "subarray_id": 1},
                "cbf": {"fsp": [{"fsp_id": 1, "function_mode": "FANTASY",
                                 "frequency_slice_id": 1,
                                 "integration_factor": 10,
                                 "zoom_factor": 0,
                                 "channel_averaging_map": [[0, 2], [744, 0]],
                                 "channel_offset": 0,
                                 "output_link_map": [[0, 0], [200, 1]]},
                                {"fsp_id": 2, "function_mode": "FANTASY",
                                 "frequency_slice_id": 2,
                                 "integration_factor": 10,
                                 "zoom_factor": 0,
                                 "channel_averaging_map": [[0, 2], [744, 0]],
                                 "channel_offset": 744,
                                 "output_link_map": [[0, 4], [200, 5]]}],
                        "vlbi": {}},
                "pss": {}}


def test_schema_validation_call_ska_telescope_validate_method():
    """
     Verify  schema validation with test valid json
    """
    with mock.patch('ska_telmodel.schema.validate') as mock_fn:
        json_schema_obj = JsonSchema()
        json_schema_obj.validate_schema(uri=VALID_JSON["interface"],
                                        instance=VALID_JSON)
    mock_fn.assert_called_once()


# TODO remove before merging AT2-855
@pytest.mark.xfail
def test_schema_validation_with_valid_json():
    """
     Verify  schema validation with test valid json
    """

    json_schema_obj = JsonSchema()
    response = json_schema_obj.validate_schema(uri=VALID_JSON["interface"],
                                               instance=VALID_JSON)
    assert response is None


def test_schema_validation_with_invalid_json():
    """
     Verify  schema validation with test invalid json where interface uri is specified
     with wrong version number and functionMode has invalid value
    """
    json_schema_obj = JsonSchema()
    with pytest.raises(ValueError):
        json_schema_obj.validate_schema(uri=INVALID_JSON["interface"],
                                        instance=INVALID_JSON)


def test_schema_with_invalid_uri():
    """
      Verify schema with invalid uri raise exception
    """
    json_schema_obj = JsonSchema()
    with pytest.raises(ValueError):
        json_schema_obj.get_schema_by_uri(uri=INVALID_JSON["interface"])


def test_get_schema_by_uri():
    """
      Verify schema with valid uri
    """
    with mock.patch('ska_telmodel.schema.schema_by_uri') as mock_fn:
        json_schema_obj = JsonSchema()
        schema = json_schema_obj.get_schema_by_uri(uri=VALID_JSON["interface"])
    assert schema is not None
    mock_fn.assert_called_once()

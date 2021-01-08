"""
Unit tests for the ska.cdm.schemas.subarray_node.configure.csp module.

This is an equivalent set of tests to test_csp.py but with the ADR-18 changes.
"""
import copy
import inspect

from ska.cdm.messages.subarray_node.configure.csp import (
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    CBFConfiguration,
    SubarrayConfiguration,
    CommonConfiguration,
)
from ska.cdm.messages.subarray_node.configure.core import ReceiverBand
from ska.cdm.schemas.subarray_node.configure import (
    CSPConfigurationSchema,
    FSPConfigurationSchema,
    CBFConfigurationSchema,
    SubarrayConfigurationSchema,
    CommonConfigurationSchema,
)
from ska.cdm.utils import json_is_equal


########################
# FSPConfiguration tests
########################

VALID_FSPCONFIGURATION_JSON = """
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
}"""


def test_marshall_fsp_configuration():
    """
    Verify that FSPConfiguration is marshalled to JSON correctly.
    """
    fsp_config = FSPConfiguration(
        2,
        FSPFunctionMode.CORR,
        2,
        1400,
        1,
        channel_averaging_map=[(0, 2), (744, 0)],
        fsp_channel_offset=744,
        output_link_map=[(0, 4), (200, 5)],
        zoom_window_tuning=4700000
    )
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)

    assert json_is_equal(marshalled, VALID_FSPCONFIGURATION_JSON)


def test_unmarshall_fsp_configuration():
    """
    Verify that FSPConfiguration is marshalled to JSON correctly.
    """
    fsp_config = FSPConfiguration(
        2,
        FSPFunctionMode.CORR,
        2,
        1400,
        1,
        channel_averaging_map=[(0, 2), (744, 0)],
        fsp_channel_offset=744,
        output_link_map=[(0, 4), (200, 5)],
        zoom_window_tuning=4700000
    )
    unmarshalled = FSPConfigurationSchema().loads(VALID_FSPCONFIGURATION_JSON)

    assert fsp_config == unmarshalled


VALID_FSPCONFIGURATION_JSON_OLM = """
{
  "fspID": 1,
  "functionMode": "CORR",
  "frequencySliceID": 1,
  "integrationTime": 1400,
  "corrBandwidth": 0,
  "outputLinkMap": [[1,0], [201,1]]
}"""


def test_marshall_fsp_configuration_with_olm():
    """
    Verify that FSPConfiguration is marshalled to JSON correctly
    when only Output Link Map is present out of optional parameters.
    """
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        output_link_map=[(1, 0), (201, 1)],
    )
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)

    assert json_is_equal(marshalled, VALID_FSPCONFIGURATION_JSON_OLM)


def test_unmarshall_fsp_configuration_with_olm():
    """
    Verify that FSPConfiguration is unmarshalled from JSON correctly
    when only Output Link Map is present out of optional parameters.
    """
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        output_link_map=[(1, 0), (201, 1)],
    )
    unmarshalled = FSPConfigurationSchema().loads(VALID_FSPCONFIGURATION_JSON_OLM)

    assert fsp_config == unmarshalled


VALID_FSPCONFIGURATION_JSON_FCO = """
{
  "fspID": 1,
  "functionMode": "CORR",
  "frequencySliceID": 1,
  "integrationTime": 1400,
  "corrBandwidth": 0,
  "fspChannelOffset": 12
}"""


def test_marshall_fsp_configuration_with_fco():
    """
    Verify that FSPConfiguration is marshalled to JSON correctly
    when only FSP Channel Offset is present out of optional parameters.
    """
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        fsp_channel_offset=12
    )
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)

    assert json_is_equal(marshalled, VALID_FSPCONFIGURATION_JSON_FCO)


def test_unmarshall_fsp_configuration_with_fco():
    """
    Verify that FSPConfiguration is unmarshalled from JSON correctly
    when only FSP Channel Offset is present out of optional parameters.
    """
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        fsp_channel_offset=12
    )
    unmarshalled = FSPConfigurationSchema().loads(VALID_FSPCONFIGURATION_JSON_FCO)

    assert fsp_config == unmarshalled


VALID_FSPCONFIGURATION_JSON_ZOOM = """
{
  "fspID": 1,
  "functionMode": "CORR",
  "frequencySliceID": 1,
  "integrationTime": 1400,
  "corrBandwidth": 0,
  "zoomWindowTuning": 4700000
}"""


def test_marshall_fsp_configuration_with_zoom():
    """
    Verify that FSPConfiguration is marshalled to JSON correctly
    when only Zoom Window Tuning is present out of optional parameters.
    """
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        zoom_window_tuning=4700000
    )
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)

    assert json_is_equal(marshalled, VALID_FSPCONFIGURATION_JSON_ZOOM)


def test_unmarshall_fsp_configuration_with_zoom():
    """
    Verify that FSPConfiguration is unmarshalled from JSON correctly
    when only Zoom Window Tuning is present out of optional parameters.
    """
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        zoom_window_tuning=4700000
    )
    unmarshalled = FSPConfigurationSchema().loads(VALID_FSPCONFIGURATION_JSON_ZOOM)

    assert fsp_config == unmarshalled


def test_marshall_fsp_configuration_with_undefined_optional_parameters():
    """
    Verify that optional FSPConfiguration parameters are removed when they are
    left unset.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)

    optional_fields = [
        field.data_key
        for name, field in schema.fields.items()
        if field.required is False
    ]
    for field in optional_fields:
        assert field not in marshalled


def test_unmarshall_fsp_configuration_without_optional_parameters():
    """
    Verify that FSPConfiguration is unmarshalled correctly when optional
    parameters are not present in JSON.
    """
    valid_json = """
    {
      "fspID": 1,
      "functionMode": "CORR",
      "frequencySliceID": 1,
      "integrationTime": 1400,
      "corrBandwidth": 0
    }
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    unmarshalled = FSPConfigurationSchema().loads(valid_json)

    assert fsp_config == unmarshalled


def test_marshall_fsp_configuration_with_optional_parameters_as_none():
    """
    Verify that optional FSPConfiguration parameters are removed when None is
    passed in as their constructor value.
    """
    constructor_signature = inspect.signature(FSPConfiguration.__init__)
    optional_kwarg_names = [
        name
        for name, parameter in constructor_signature.parameters.items()
        if parameter.kind == inspect.Parameter.KEYWORD_ONLY
    ]
    null_kwargs = {name: None for name in optional_kwarg_names}

    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0, **null_kwargs)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)

    # optional constructor args are optional fields in the schema
    optional_fields = [
        field.data_key
        for name, field in schema.fields.items()
        if field.required is False
    ]
    for field in optional_fields:
        assert field not in marshalled


########################
# SubarrayConfiguration tests
########################

VALID_SUBARRAYCONFIGURATION_JSON = """
{
  "subarrayName": "Test Subarray"
}
"""


def test_marshall_subarray_configuration():
    """
    Verify that SubarrayConfiguration is marshalled to JSON correctly.
    """
    subarray_config = SubarrayConfiguration("Test Subarray")
    schema = SubarrayConfigurationSchema()
    marshalled = schema.dumps(subarray_config)
    assert json_is_equal(marshalled, VALID_SUBARRAYCONFIGURATION_JSON)


def test_unmarshall_subarray_configuration():
    """
    Verify that SubarrayConfiguration is unmarshalled from JSON correctly.
    """
    subarray_config = SubarrayConfiguration("Test Subarray")
    schema = SubarrayConfigurationSchema()
    unmarshalled = schema.loads(VALID_SUBARRAYCONFIGURATION_JSON)

    assert subarray_config == unmarshalled


########################
# CommonConfiguration tests
########################

VALID_COMMONCONFIGURATION_JSON = """
{
  "id": "123",
  "frequencyBand": "1",
  "subarrayID": 1
}
"""


def test_marshall_common_configuration():
    """
    Verify that CommonConfiguration is marshalled to JSON correctly.
    """
    common_config = CommonConfiguration("123", ReceiverBand.BAND_1, 1)
    schema = CommonConfigurationSchema()
    marshalled = schema.dumps(common_config)
    assert json_is_equal(marshalled, VALID_COMMONCONFIGURATION_JSON)


def test_unmarshall_common_configuration():
    """
    Verify that CommonConfiguration is unmarshalled from JSON correctly.
    """
    common_config = CommonConfiguration("123", ReceiverBand.BAND_1, 1)
    schema = CommonConfigurationSchema()
    unmarshalled = schema.loads(VALID_COMMONCONFIGURATION_JSON)

    assert common_config == unmarshalled


########################
# CBFConfiguration tests
########################

VALID_CBFCONFIGURATION_JSON = """
{
  "fsp": [
    {
      "fspID": 1,
      "functionMode": "CORR",
      "frequencySliceID": 1,
      "integrationTime": 1400,
      "corrBandwidth": 0,
      "channelAveragingMap": [[0, 2], [744, 0]],
      "outputLinkMap": [[0,0], [200,1]],
      "fspChannelOffset": 0
    }
  ]
}
"""


def test_marshall_cbf_configuration():
    """
    Verify that CBFConfiguration is marshalled to JSON correctly.
    """
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_averaging_map=[(0, 2), (744, 0)],
        fsp_channel_offset=0,
        output_link_map=[(0, 0), (200, 1)]
    )
    cbf_config = CBFConfiguration([fsp_config])
    schema = CBFConfigurationSchema()
    marshalled = schema.dumps(cbf_config)
    assert json_is_equal(marshalled, VALID_CBFCONFIGURATION_JSON)


def test_unmarshall_cbf_configuration():
    """
    Verify that CBFConfiguration is unmarshalled from JSON correctly.
    """
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_averaging_map=[(0, 2), (744, 0)],
        fsp_channel_offset=0,
        output_link_map=[(0, 0), (200, 1)]
    )
    cbf_config = CBFConfiguration([fsp_config])
    schema = CBFConfigurationSchema()
    unmarshalled = schema.loads(VALID_CBFCONFIGURATION_JSON)

    assert cbf_config == unmarshalled


########################
# CSPConfiguration tests
########################

VALID_CSPCONFIGURATION_JSON = """
{
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


def test_marshall_cspconfiguration():
    """
    Verify that CSPConfiguration is marshalled to JSON correctly.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
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
        common_element_config=csp_common_config,
        cbf_config=cbf_config
    )
    schema = CSPConfigurationSchema()
    marshalled = schema.dumps(csp_config)
    assert json_is_equal(marshalled, VALID_CSPCONFIGURATION_JSON)


def test_unmarshall_cspconfiguration():
    """
    Verify that CSPConfiguration is unmarshalled from JSON correctly.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
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
        common_element_config=csp_common_config,
        cbf_config=cbf_config
    )
    schema = CSPConfigurationSchema()
    unmarshalled = schema.loads(VALID_CSPCONFIGURATION_JSON)

    assert csp_config == unmarshalled


def test_marshall_cspconfiguration_does_not_modify_original():
    """
    Verify that serialising a CspConfiguration does not change the object.
    """
    cbf_config = CBFConfiguration(
        [FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)]
    )
    csp_subarray_config = SubarrayConfiguration('science period 23')
    csp_common_config = CommonConfiguration('123', ReceiverBand.BAND_1, 1)
    config = CSPConfiguration(
        subarray_config=csp_subarray_config,
        common_element_config=csp_common_config,
        cbf_config=cbf_config
    )
    original_config = copy.deepcopy(config)
    CSPConfigurationSchema().dumps(config)
    assert config == original_config

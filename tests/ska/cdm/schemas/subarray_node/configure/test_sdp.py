"""
Unit tests for the ska.cdm.schemas.subarray_node.configure.sdp module.
"""
import ska.cdm.messages.subarray_node as sn
from ska.cdm.schemas.subarray_node.configure.sdp import SDPConfigurationSchema
from tests.ska.cdm.schemas.utils import json_is_equal

VALID_SDP_CONFIGURE_SB = """
{
    "configure": [
      {
        "id": "realtime-20190627-0001",
        "sbiId": "20190627-0001",
        "workflow": {
          "id": "vis_ingest",
          "type": "realtime",
          "version": "0.1.0"
        },
        "parameters": {
          "numStations": 4,
          "numChannels": 372,
          "numPolarisations": 4,
          "freqStartHz": 0.35e9,
          "freqEndHz": 1.05e9,
          "fields": {
            "0": { "system": "ICRS", "name": "NGC6251", "ra": 1.0, "dec": 1.0 }
          }
        },
        "scanParameters": {
          "12345": { "fieldId": 0, "intervalMs": 1400 }
        }
      }
    ]
}
"""

VALID_SDP_CONFIGURE_SCAN = """
{
    "configureScan": {
      "scanParameters": {
        "12346": { "fieldId": 0, "intervalMs": 2800 }
      }
    }
}
"""

VALID_SDP_CONFIGURE_AND_CONFIGURE_SCAN = """
{
    "configure": [
      {
        "id": "realtime-20190627-0001",
        "sbiId": "20190627-0001",
        "workflow": {
          "id": "vis_ingest",
          "type": "realtime",
          "version": "0.1.0"
        },
        "parameters": {
          "numStations": 4,
          "numChannels": 372,
          "numPolarisations": 4,
          "freqStartHz": 0.35e9,
          "freqEndHz": 1.05e9,
          "fields": {
            "0": { "system": "ICRS", "name": "NGC6251", "ra": 1.0, "dec": 1.0 }
          }
        },
        "scanParameters": {
          "12345": { "fieldId": 0, "intervalMs": 1400 }
        }
      }
    ],
    "configureScan": {
      "scanParameters": {
        "12346": { "fieldId": 0, "intervalMs": 2800 }
      }
    }
}
"""


def get_sdp_scan_configuration_for_test(scan_id) -> sn.SDPConfiguration:
    """
    Utility method to create an SDPScanParameters for use in tests
    """
    scan_list = {str(scan_id): sn.SDPScan(field_id=0, interval_ms=2800)}
    scan_config = sn.SDPScanParameters(scan_list)
    return sn.SDPConfiguration(configure_scan=scan_config)


def test_marshal_sdp_configure_scan():
    """
    Verify that SDP scan configuration can be marshalled to JSON correctly
    """
    scan_config = get_sdp_scan_configuration_for_test(12346)
    schema = SDPConfigurationSchema()
    result = schema.dumps(scan_config)
    assert json_is_equal(result, VALID_SDP_CONFIGURE_SCAN)


def test_unmarshall_sdp_configure_scan():
    """
    Verify that JSON can be unmarshalled back to a ConfigureScan
    """
    schema = SDPConfigurationSchema()
    result = schema.loads(VALID_SDP_CONFIGURE_SCAN)
    assert '12346' in result.configure_scan.scan_parameters


def test_marshal_sdp_configure_request():
    """
    Verify that JSON can be marshalled to JSON correctly
    """
    sb_id = 'realtime-20190627-0001'
    sbi_id = '20190627-0001'
    target = sn.Target(ra=1.0, dec=1.0, name='NGC6251', unit='rad')
    target_list = {'0': target}

    workflow = sn.SDPWorkflow(workflow_id='vis_ingest', workflow_type='realtime', version='0.1.0')

    parameters = sn.SDPParameters(num_stations=4, num_channels=372,
                                  num_polarisations=4, freq_start_hz=0.35e9,
                                  freq_end_hz=1.05e9, target_fields=target_list)
    scan = sn.SDPScan(field_id=0, interval_ms=1400)
    scan_list = {'12345': scan}

    pb_config = sn.ProcessingBlockConfiguration(sb_id=sb_id,
                                                sbi_id=sbi_id,
                                                workflow=workflow,
                                                parameters=parameters,
                                                scan_parameters=scan_list)

    sdp_configure = sn.SDPConfiguration([pb_config])
    schema = SDPConfigurationSchema()
    result = schema.dumps(sdp_configure)

    assert json_is_equal(result, VALID_SDP_CONFIGURE_SB)


def test_marshal_sdp_configure_scan_request():
    """
    Verify that SDP scan configuration can be marshalled to JSON correctly
    """
    sdp_config = get_sdp_scan_configuration_for_test(12346)
    schema = SDPConfigurationSchema()
    result = schema.dumps(sdp_config)
    assert json_is_equal(result, VALID_SDP_CONFIGURE_SCAN)


def test_unmarshall_sdp_configure_request():
    """
    Verify that JSON can be unmarshalled back to an SDP SB configuration
    """
    schema = SDPConfigurationSchema()
    result = schema.loads(VALID_SDP_CONFIGURE_SB)
    config_block = result.configure[0]
    assert isinstance(config_block, sn.ProcessingBlockConfiguration)


def test_unmarshall_sdp_configure_scan_request():
    """
    Verify that JSON can be unmarshalled back to a ScanRequest
    """
    schema = SDPConfigurationSchema()
    result = schema.loads(VALID_SDP_CONFIGURE_SCAN)
    assert '12346' in result.configure_scan.scan_parameters


def test_unmarshall_both_sdp_configure_and_configure_scan_request():
    """
    Verify that SB- and scan-level configurations can be unmarshalled and
    co-exist in the same SDPConfiguration.
    """
    schema = SDPConfigurationSchema()
    result = schema.loads(VALID_SDP_CONFIGURE_AND_CONFIGURE_SCAN)
    assert isinstance(result.configure, list)
    assert isinstance(result.configure_scan, sn.SDPScanParameters)


def test_unmarshall_empty_sdp_configure_request():
    """
    Nominal test  - more for documentation - since both configure and confgureScan are optional
    it is technically possible to have an sdp configuration that is empty.
    Placeholder for a test if we close this down.
    """
    schema = SDPConfigurationSchema()
    result = schema.loads('{}')
    assert result == sn.SDPConfiguration()

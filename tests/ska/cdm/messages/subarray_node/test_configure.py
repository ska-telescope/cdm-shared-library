"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import itertools

from ska.cdm.messages.subarray_node.configure import ConfigureRequest
from ska.cdm.messages.subarray_node.configure.common import PointingConfiguration, \
    DishConfiguration, Target, ReceiverBand
from ska.cdm.messages.subarray_node.configure.csp import FSPConfiguration, FSPFunctionMode, \
    CSPConfiguration
from ska.cdm.messages.subarray_node.configure.sdp import SDPWorkflow, SDPParameters, SDPScan, \
    ProcessingBlockConfiguration, SDPConfiguration


def get_sdp_configuration_for_test(target):
    """
    Quick method for setting up an SDP Configure that can be used for testing
    For completeness of testing it also does the tests to ensure that if classes
    are of different types they are considered unequal
    """
    target_list = {'0': target}
    workflow = SDPWorkflow(workflow_id='vis_ingest', workflow_type='realtime', version='0.1.0')

    parameters = SDPParameters(num_stations=4, num_channels=372, num_polarisations=4,
                               freq_start_hz=0.35e9, freq_end_hz=1.05e9, target_fields=target_list)

    scan = SDPScan(field_id=0, interval_ms=1400)

    scan_list = {'12345': scan}
    pb_config = ProcessingBlockConfiguration(sb_id='realtime-20190627-0001', sbi_id='20190627-0001',
                                             workflow=workflow, parameters=parameters,
                                             scan_parameters=scan_list)

    sdp_config = SDPConfiguration(configure=[pb_config])

    return sdp_config


def test_configure_request_eq():
    """
    Verify that ConfigurationRequest objects are considered equal when:
      - they have the same scan ID
      - they point to the same target
      - they set the same receiver band
      - their SDP configuration is the same
      - their CSP configuration is the same
    """
    scan_id = 123

    pointing_config = PointingConfiguration(Target(1, 1))
    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    sdp_config = get_sdp_configuration_for_test(Target(1, 1))
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, 0, channel_avg_map)
    csp_config = CSPConfiguration(scan_id, ReceiverBand.BAND_1, [fsp_config])
    request_1 = ConfigureRequest(scan_id, pointing_config, dish_config, sdp_config, csp_config)

    pointing_config = PointingConfiguration(Target(1, 1))
    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    sdp_config = get_sdp_configuration_for_test(Target(1, 1))
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, 0, channel_avg_map)
    csp_config = CSPConfiguration(scan_id, ReceiverBand.BAND_1, [fsp_config])
    request_2 = ConfigureRequest(scan_id, pointing_config, dish_config, sdp_config, csp_config)

    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest is not equal to other objects.
    """
    scan_id = 123
    pointing_config = PointingConfiguration(Target(1, 1))
    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    sdp_config = get_sdp_configuration_for_test(Target(1, 1))
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, 0, channel_avg_map)
    csp_config = CSPConfiguration(scan_id, ReceiverBand.BAND_1, [fsp_config])
    request = ConfigureRequest(scan_id, pointing_config, dish_config, sdp_config, csp_config)

    assert request != object

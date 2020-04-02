"""
Unit tests for the ska.cdm.messages.subarray_node.configure.sdp module.
"""
import ska.cdm.messages.subarray_node.configure.sdp as sdp


def test_workflow_equals():
    """
    Verify that SDP Workflow objects are considered equal when they have:
     - the same ID
     - the same type
     - the same version
    """
    workflow1 = sdp.SDPWorkflow('id', 'type', 'version')
    workflow2 = sdp.SDPWorkflow('id', 'type', 'version')
    assert workflow1 == workflow2

    assert workflow1 != sdp.SDPWorkflow('', 'type', 'version')
    assert workflow1 != sdp.SDPWorkflow('id', '', 'version')
    assert workflow1 != sdp.SDPWorkflow('id', 'type', '')


def test_workflow_not_equal_to_other_objects():
    """
    Verify that SDP Workflow objects are not considered equal to objects of
    other types.
    """
    workflow1 = sdp.SDPWorkflow('id', 'type', 'version')
    assert workflow1 != 1


def test_sdp_parameters_equals():
    """
    Verify that SDP parameters are considered equal when all attributes
    are the same.
    """
    param1 = sdp.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                               freq_start_hz=10,
                               freq_end_hz=20, target_fields={})
    param2 = sdp.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                               freq_start_hz=10,
                               freq_end_hz=20, target_fields={})
    assert param1 == param2

    assert param1 != sdp.SDPParameters(num_stations=2, num_channels=2, num_polarisations=4,
                                       freq_start_hz=10, freq_end_hz=20, target_fields={})
    assert param1 != sdp.SDPParameters(num_stations=1, num_channels=1, num_polarisations=4,
                                       freq_start_hz=10, freq_end_hz=20, target_fields={})
    assert param1 != sdp.SDPParameters(num_stations=1, num_channels=2, num_polarisations=2,
                                       freq_start_hz=10, freq_end_hz=20, target_fields={})
    assert param1 != sdp.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                                       freq_start_hz=20, freq_end_hz=20, target_fields={})
    assert param1 != sdp.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                                       freq_start_hz=10, freq_end_hz=30, target_fields={})
    assert param1 != sdp.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                                       freq_start_hz=10, freq_end_hz=20, target_fields={'a': 0})


def test_sdp_parameters_not_equal_to_other_objects():
    """
    Verify that SDPParameters objects are not considered equal to objects of
    other types.
    """
    param = sdp.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4, freq_start_hz=10,
                              freq_end_hz=20, target_fields={})
    assert param != 1


def test_sdp_scan_equals():
    """
    Verify that SDPScan are considered equal when all attributes are equal.
    """
    scan1 = sdp.SDPScan(1, 2)
    scan2 = sdp.SDPScan(1, 2)
    assert scan1 == scan2

    assert scan1 != sdp.SDPScan(2, 2)
    assert scan1 != sdp.SDPScan(2, 1)


def test_sdp_scan_not_equal_to_other_objects():
    """
    Verify that SDPScan objects are not considered equal to objects of other
    types.
    """
    scan = sdp.SDPScan(1, 2)
    assert scan != 1


def test_sdp_scan_parameters_equals():
    """
    Verify that SDPScanParameters are considered equal when all attributes are
    equal.
    """
    param1 = sdp.SDPScanParameters({'0': sdp.SDPScan(1, 2)})
    param2 = sdp.SDPScanParameters({'0': sdp.SDPScan(1, 2)})
    assert param1 == param2

    assert param1 != sdp.SDPScanParameters({'1': sdp.SDPScan(1, 2)})
    assert param1 != sdp.SDPScanParameters({})


def test_sdp_scan_parameters_not_equal_to_other_objects():
    """
    Verify that SDPScanParameters objects are not considered equal to objects
    of other types.
    """
    param = sdp.SDPScanParameters({'0': sdp.SDPScan(1, 2)})
    assert param != 1


def test_processing_block_configuration_not_equal_to_other_objects():
    """
    Verify that ProcessingBlockConfiguration objects are not considered equal
    to objects of other types.
    """
    config = sdp.ProcessingBlockConfiguration(None, None, None, None, None)
    assert config != 1


def test_sdp_configure_scan_comparisons():
    """
    Basic check for the SDP message objects not tested above that if classes
    are of different types they cannot have the same value
    """
    scan = sdp.SDPScan(field_id=0, interval_ms=2800)

    scan_parameters = sdp.SDPScanParameters({"12345": scan})

    configure_scan = sdp.SDPConfiguration(configure_scan=scan_parameters)
    assert configure_scan != object

"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import ska.cdm.messages.subarray_node.configure as configure


def get_sdp_configuration_for_test(target):
    """
    Quick method for setting up an SDP Configure that can be used for testing
    For completeness of testing it also does the tests to ensure that if classes
    are of different types they are considered unequal
    """
    target_list = {'0': target}
    workflow = configure.SDPWorkflow(workflow_id='vis_ingest',
                                     workflow_type='realtime',
                                     version='0.1.0')

    parameters = configure.SDPParameters(num_stations=4, num_channels=372,
                                         num_polarisations=4, freq_start_hz=0.35e9,
                                         freq_end_hz=1.05e9, target_fields=target_list)

    scan = configure.SDPScan(field_id=0, interval_ms=1400)

    scan_list = {'12345': scan}
    pb_config = configure.ProcessingBlockConfiguration(sb_id='realtime-20190627-0001',
                                                       sbi_id='20190627-0001',
                                                       workflow=workflow,
                                                       parameters=parameters,
                                                       scan_parameters=scan_list)

    sdp_config = configure.SDPConfiguration(configure=[pb_config])

    return sdp_config


def test_sdp_configure_scan_comparisons():
    """
    Basic check for the SDP message objects not tested above that if classes
    are of different types they cannot have the same value
    """
    scan = configure.SDPScan(field_id=0, interval_ms=2800)

    scan_parameters = configure.SDPScanParameters({"12345": scan})

    configure_scan = configure.SDPConfiguration(configure_scan=scan_parameters)
    assert configure_scan != object


def test_target_defaults():
    """
    Verify Target default arguments.
    """
    target_1 = configure.Target(ra=1, dec=0.5)
    target_2 = configure.Target(ra=1, dec=0.5, name='', frame='icrs', unit=('hourangle', 'deg'))
    assert target_1 == target_2


def test_target_eq():
    """
    Verify that Target objects are considered equal when:

      - they have the same name
      - they point to the same place on the sky
      - they use the same co-ordinate frame
      - they use the same co-ordinate units
    """
    target_1 = configure.Target(ra=1, dec=2, name='a source', frame='fk5', unit='deg')
    target_2 = configure.Target(ra=1, dec=2, name='a source', frame='fk5', unit='deg')
    target_3 = configure.Target(ra=1, dec=1)
    assert target_1 == target_2
    assert target_1 != target_3


def test_target_is_not_equal_to_other_objects():
    """
    Verify that Target objects are considered unequal to other objects.
    """
    target = configure.Target(ra=1, dec=2, name='a source', frame='fk5', unit='deg')
    assert target != object


def test_target_repr():
    """
    Verify the repr representation of a Target.
    """
    target = configure.Target(ra=30, dec=-3600, name='name', frame='icrs', unit=('deg', 'arcsec'))
    expected = "<Target(ra=30.0, dec=-1.0, name='name', frame='icrs', unit=('deg', 'deg'))>"
    assert expected == repr(target)


def test_target_str():
    """
    Verify the string representation of a Target.
    """
    target = configure.Target(ra=30, dec='0', name='name', frame='icrs', unit=('deg', 'rad'))
    expected = "<Target: 'name' (02h00m00s +00d00m00s icrs)>"
    assert expected == str(target)


def test_pointing_configuration_eq():
    """
    Verify that PointingConfiguration objects are considered equal when:
      - they point to the same target
    """
    target_1 = configure.Target(ra=1, dec=2, name='a source', frame='fk5', unit='deg')
    target_2 = configure.Target(ra=1, dec=2, name='a source', frame='fk5', unit='deg')
    target_3 = configure.Target(ra=1, dec=2, name='foobar', frame='fk4', unit='deg')
    config_1 = configure.PointingConfiguration(target_1)
    config_2 = configure.PointingConfiguration(target_2)
    config_3 = configure.PointingConfiguration(target_3)
    assert config_1 == config_2
    assert config_1 != config_3


def test_pointing_configuration_is_not_equal_to_other_objects():
    """
    Verify that PointingConfiguration is not considered equal to
    non-PointingConfiguration objects.
    """
    target = configure.Target(ra=1, dec=2, name='a source', frame='fk5', unit='deg')
    config = configure.PointingConfiguration(target)
    assert config != object


def test_dish_configuration_eq():
    """
    Verify that DishConfiguration objects are considered equal when:
      - they use the same receiver band
    """
    config_1 = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    config_2 = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    config_3 = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_2)
    assert config_1 == config_2
    assert config_1 != config_3


def test_dish_configuration_is_not_equal_to_other_objects():
    """
    Verify that DishConfiguration is considered unequal to
    non-DishConfiguration objects.
    :return:
    """
    config_1 = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    assert config_1 != configure.Target(1, 1)
    assert config_1 != object


def test_configure_request_eq():
    """
    Verify that ConfigurationRequest objects are considered equal when:
      - they have the same scan ID
      - they point to the same target
      - they set the same receiver band
      - their SDP configuration is the same
      - their CSP configuration is the same
    """
    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    sdp_config = get_sdp_configuration_for_test(configure.Target(1, 1))
    channel_avg_map = [(1, 2), (745, 0), (1489, 0), (2233, 0), (2977, 0), (3721, 0), (4465, 0),
                       (5209, 0), (5953, 0), (6697, 0), (7441, 0), (8185, 0), (8929, 0), (9673, 0), (10417, 0),
                       (11161, 0), (11905, 0), (12649, 0), (13393, 0), (14137, 0)]
    scan_id = 123
    fsp_config = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = configure.CSPConfiguration(scan_id, configure.ReceiverBand.BAND_1, [fsp_config])
    request_1 = configure.ConfigureRequest(123, pointing_config, dish_config, sdp_config, csp_config)

    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    sdp_config = get_sdp_configuration_for_test(configure.Target(1, 1))
    channel_avg_map = [(1, 2), (745, 0), (1489, 0), (2233, 0), (2977, 0), (3721, 0), (4465, 0),
                       (5209, 0), (5953, 0), (6697, 0), (7441, 0), (8185, 0), (8929, 0), (9673, 0), (10417, 0),
                       (11161, 0), (11905, 0), (12649, 0), (13393, 0), (14137, 0)]
    scan_id = 123
    fsp_config = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = configure.CSPConfiguration(scan_id, configure.ReceiverBand.BAND_1, [fsp_config])
    request_2 = configure.ConfigureRequest(123, pointing_config, dish_config, sdp_config, csp_config)

    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest is not equal to other objects.
    """
    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    sdp_config = get_sdp_configuration_for_test(configure.Target(1, 1))
    channel_avg_map = [(1, 2), (745, 0), (1489, 0), (2233, 0), (2977, 0), (3721, 0), (4465, 0),
                       (5209, 0), (5953, 0), (6697, 0), (7441, 0), (8185, 0), (8929, 0), (9673, 0), (10417, 0),
                       (11161, 0), (11905, 0), (12649, 0), (13393, 0), (14137, 0)]
    scan_id = 123
    fsp_config = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = configure.CSPConfiguration(scan_id, configure.ReceiverBand.BAND_1, [fsp_config])
    request = configure.ConfigureRequest(123, pointing_config, dish_config, sdp_config, csp_config)

    assert request != object


def test_workflow_equals():
    """
    Verify that SDP Workflow objects are considered equal when they have:
     - the same ID
     - the same type
     - the same version
    """
    workflow1 = configure.SDPWorkflow('id', 'type', 'version')
    workflow2 = configure.SDPWorkflow('id', 'type', 'version')
    assert workflow1 == workflow2

    assert workflow1 != configure.SDPWorkflow('', 'type', 'version')
    assert workflow1 != configure.SDPWorkflow('id', '', 'version')
    assert workflow1 != configure.SDPWorkflow('id', 'type', '')


def test_workflow_not_equal_to_other_objects():
    """
    Verify that SDP Workflow objects are not considered equal to objects of
    other types.
    """
    workflow1 = configure.SDPWorkflow('id', 'type', 'version')
    assert workflow1 != 1


def test_sdp_parameters_equals():
    """
    Verify that SDP parameters are considered equal when all attributes
    are the same.
    """
    param1 = configure.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                                     freq_start_hz=10, freq_end_hz=20, target_fields={})
    param2 = configure.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                                     freq_start_hz=10, freq_end_hz=20, target_fields={})
    assert param1 == param2

    assert param1 != configure.SDPParameters(num_stations=2, num_channels=2, num_polarisations=4,
                                             freq_start_hz=10, freq_end_hz=20, target_fields={})
    assert param1 != configure.SDPParameters(num_stations=1, num_channels=1, num_polarisations=4,
                                             freq_start_hz=10, freq_end_hz=20, target_fields={})
    assert param1 != configure.SDPParameters(num_stations=1, num_channels=2, num_polarisations=2,
                                             freq_start_hz=10, freq_end_hz=20, target_fields={})
    assert param1 != configure.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                                             freq_start_hz=20, freq_end_hz=20, target_fields={})
    assert param1 != configure.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                                             freq_start_hz=10, freq_end_hz=30, target_fields={})
    assert param1 != configure.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                                             freq_start_hz=10, freq_end_hz=20,
                                             target_fields={'a': 0})


def test_sdp_parameters_not_equal_to_other_objects():
    """
    Verify that SDPParameters objects are not considered equal to objects of
    other types.
    """
    param = configure.SDPParameters(num_stations=1, num_channels=2, num_polarisations=4,
                                    freq_start_hz=10, freq_end_hz=20, target_fields={})
    assert param != 1


def test_sdp_scan_equals():
    """
    Verify that SDPScan are considered equal when all attributes are equal.
    """
    scan1 = configure.SDPScan(1, 2)
    scan2 = configure.SDPScan(1, 2)
    assert scan1 == scan2

    assert scan1 != configure.SDPScan(2, 2)
    assert scan1 != configure.SDPScan(2, 1)


def test_sdp_scan_not_equal_to_other_objects():
    """
    Verify that SDPScan objects are not considered equal to objects of other
    types.
    """
    scan = configure.SDPScan(1, 2)
    assert scan != 1


def test_sdp_scan_parameters_equals():
    """
    Verify that SDPScanParameters are considered equal when all attributes are
    equal.
    """
    param1 = configure.SDPScanParameters({'0': configure.SDPScan(1, 2)})
    param2 = configure.SDPScanParameters({'0': configure.SDPScan(1, 2)})
    assert param1 == param2

    assert param1 != configure.SDPScanParameters({'1': configure.SDPScan(1, 2)})
    assert param1 != configure.SDPScanParameters({})


def test_sdp_scan_parameters_not_equal_to_other_objects():
    """
    Verify that SDPScanParameters objects are not considered equal to objects
    of other types.
    """
    param = configure.SDPScanParameters({'0': configure.SDPScan(1, 2)})
    assert param != 1


def test_processing_block_configuration_not_equal_to_other_objects():
    """
    Verify that ProcessingBlockConfiguration objects are not considered equal
    to objects of other types.
    """
    config = configure.ProcessingBlockConfiguration(None, None, None, None, None)
    assert config != 1

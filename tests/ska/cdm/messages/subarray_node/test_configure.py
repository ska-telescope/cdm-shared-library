"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import itertools
import functools
import pytest

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
    scan_id = 123

    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    sdp_config = get_sdp_configuration_for_test(configure.Target(1, 1))
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    fsp_config = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 140, 0,
                                            channel_avg_map)
    csp_config = configure.CSPConfiguration(scan_id, configure.ReceiverBand.BAND_1, [fsp_config])
    request_1 = configure.ConfigureRequest(scan_id, pointing_config, dish_config, sdp_config,
                                           csp_config)

    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    sdp_config = get_sdp_configuration_for_test(configure.Target(1, 1))
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    fsp_config = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 140, 0,
                                            channel_avg_map)
    csp_config = configure.CSPConfiguration(scan_id, configure.ReceiverBand.BAND_1, [fsp_config])
    request_2 = configure.ConfigureRequest(scan_id, pointing_config, dish_config, sdp_config,
                                           csp_config)

    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest is not equal to other objects.
    """
    scan_id = 123
    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    sdp_config = get_sdp_configuration_for_test(configure.Target(1, 1))
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    fsp_config = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 140, 0,
                                            channel_avg_map)
    csp_config = configure.CSPConfiguration(scan_id, configure.ReceiverBand.BAND_1, [fsp_config])
    request = configure.ConfigureRequest(scan_id, pointing_config, dish_config, sdp_config,
                                         csp_config)

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


def test_fsp_id_range():
    """
    Verify that fsp id is in the range of 1 to 27
    """
    fsp_id = 0
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(fsp_id, configure.FSPFunctionMode.CORR, 1, 140, 0)
    fsp_id = 28
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(fsp_id, configure.FSPFunctionMode.CORR, 1, 140, 0)


def test_fsp_slice_id_range():
    """
    Verify that fsp slice id is in the range of 1 to 26
    """
    fsp_slice_id = 0
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, fsp_slice_id, 140, 0)
    fsp_slice_id = 27
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, fsp_slice_id, 140, 0)


def test_corr_bandwidth_range():
    """
    Verify that corr_bandwidth is in the range of 0 to 6
    """
    corr_bandwidth = -1
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 140, corr_bandwidth)
    corr_bandwidth = 7
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 140, corr_bandwidth)


def test_integration_time_must_be_multiple_of_140():
    """
    Verify that integration time is multiple of 140
    """
    _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 140, 0)
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 139, 0)
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 141, 0)


def test_integration_time_is_within_limits():
    """
    Verify that integration time is no greater than 1400
    """
    _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0)
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 0, 0)
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1540, 0)


def test_number_of_channel_avg_mapping_tuples():
    """
    Verify that FSPConfiguration fails if there are an invalid number of
    entries in the channel average mapping argument.
    """
    # create a partially applied FSPConfiguration constructor to save having
    # to type the arguments each time
    fsp_constructor = functools.partial(
        configure.FSPConfiguration, 1, configure.FSPFunctionMode.CORR, 1, 140, 0
    )

    # test for 19 tuples
    channel_avg_map = list(zip(itertools.count(1, 744), 19 * [0]))
    with pytest.raises(ValueError):
        _ = fsp_constructor(channel_avg_map)

    # test for 21 tuples
    channel_avg_map = list(zip(itertools.count(1, 744), 21 * [0]))
    with pytest.raises(ValueError):
        _ = fsp_constructor(channel_avg_map)


def test_fsp_configuration_equals():
    """
    Verify that FSPConfigurations are considered equal when all attributes are
    equal.
    """
    fsp_id = 1
    mode = configure.FSPFunctionMode.CORR
    slice_id = 1
    bandwidth = 0
    channel_avg_map = list(zip(itertools.count(1, 744), 20 * [0]))
    integration_time = 140

    config1 = configure.FSPConfiguration(fsp_id, mode, slice_id, integration_time, bandwidth,
                                         channel_avg_map)
    config2 = configure.FSPConfiguration(fsp_id, mode, slice_id, integration_time, bandwidth,
                                         channel_avg_map)
    assert config1 == config2

    assert config1 != configure.FSPConfiguration(2, mode, slice_id, integration_time, bandwidth,
                                                 channel_avg_map)
    assert config1 != configure.FSPConfiguration(fsp_id, configure.FSPFunctionMode.PSS_BF,
                                                 slice_id, integration_time, bandwidth,
                                                 channel_avg_map)
    assert config1 != configure.FSPConfiguration(fsp_id, mode, 2, integration_time, bandwidth,
                                                 channel_avg_map)
    assert config1 != configure.FSPConfiguration(fsp_id, mode, slice_id, 280, bandwidth,
                                                 channel_avg_map)
    assert config1 != configure.FSPConfiguration(fsp_id, mode, slice_id, integration_time, 1,
                                                 channel_avg_map)
    assert config1 != configure.FSPConfiguration(fsp_id, mode, slice_id, integration_time,
                                                 bandwidth,
                                                 list(zip(itertools.count(1, 744), 20 * [1])))


def test_fsp_configuration_not_equal_to_other_objects():
    """
    Verify that FSPConfiguration objects are not considered equal to objects
    of other types.
    """
    config = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0)
    assert config != 1


def test_csp_configuration_equals():
    """
    Verify that CSPConfiguration objects are considered equal when all
    attributes are equal.
    """
    scan_id = 123
    frequency_band = configure.ReceiverBand.BAND_1
    fsp = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0)

    config1 = configure.CSPConfiguration(scan_id, frequency_band, [fsp])
    config2 = configure.CSPConfiguration(scan_id, frequency_band, [fsp])
    assert config1 == config2

    assert config1 != configure.CSPConfiguration(1, frequency_band, [fsp])
    assert config1 != configure.CSPConfiguration(scan_id, configure.ReceiverBand.BAND_2, [fsp])
    assert config1 != configure.CSPConfiguration(scan_id, frequency_band, [fsp, fsp])


def test_csp_configuration_not_equal_to_other_objects():
    """
    Verify that CSPConfiguration objects are not considered equal to objects
    of other types.
    """
    scan_id = 123
    frequency_band = configure.ReceiverBand.BAND_1
    fsp = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0)
    config = configure.CSPConfiguration(scan_id, frequency_band, [fsp])
    assert config != 1

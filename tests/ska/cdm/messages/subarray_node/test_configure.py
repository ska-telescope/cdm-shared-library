"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import ska.cdm.messages.subarray_node.configure as configure

def sdp_configure_for_test(target):
    """
    Quick method for setting up an SDP Configure that can be used for testing
    For completeness of testing it also does the tests to ensure that if classes
    are of different types they are considered unequal
    """
    target_list = {"0": target}
    workflow = configure.SDPWorkflow(wf_id="vis_ingest", wf_type="realtime", version="0.1.0")
    assert workflow != object

    parameters = configure.SDPParameters(num_stations=4, num_chanels=372,
                                  num_polarisations=4, freq_start_hz=0.35e9,
                                  freq_end_hz=1.05e9, target_fields=target_list)
    assert parameters != object

    scan = configure.SDPScan(field_id=0, interval_ms=1400)
    assert scan != object

    scan_list = {"12345": scan}
    sdp_config_block = configure.SDPConfigurationBlock(sb_id='realtime-20190627-0001',
                                                sbi_id='20190627-0001',
                                                workflow=workflow,
                                                parameters=parameters,
                                                scan_parameters=scan_list)
    assert sdp_config_block != object

    sdp_configure = configure.SDPConfigure([sdp_config_block])
    assert sdp_configure != object

    return sdp_configure

def test_sdp_configure_scan_comparisons():
    """
    Basic check for the SDP message objects not tested above that if classes
    are of different types they cannot have the same value
    """
    scan = configure.SDPScan(field_id=0, interval_ms=2800)

    scan_parameters = configure.SDPScanParameters({"12345": scan})
    assert scan_parameters != object

    configure_scan = configure.SDPConfigureScan(scan_parameters)
    assert  configure_scan != object





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
    """
    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    sdp_config = sdp_configure_for_test(configure.Target(1, 1))
    request_1 = configure.ConfigureRequest(123, pointing_config, dish_config, sdp_config)

    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    sdp_config = sdp_configure_for_test(configure.Target(1, 1))
    request_2 = configure.ConfigureRequest(123, pointing_config, dish_config, sdp_config)

    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest is not equal to other objects.
    """
    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    sdp_config = sdp_configure_for_test(configure.Target(1, 1))
    request = configure.ConfigureRequest(123, pointing_config, dish_config, sdp_config)
    assert request != object





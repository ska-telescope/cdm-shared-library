"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import ska.cdm.messages.subarray_node.configure as configure
import pytest

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
      - their CSP configuration is the same
    """
    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    channel_avg_map = [(1, 2), (745, 0), (1489, 0), (2233, 0), (2977, 0), (3721, 0), (4465, 0),
                       (5209, 0), (5953, 0), (6697, 0), (7441, 0), (8185, 0), (8929, 0), (9673, 0), (10417, 0),
                       (11161, 0), (11905, 0), (12649, 0), (13393, 0), (14137, 0)]
    scan_id = 123
    fsp_config = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = configure.CSPConfiguration(scan_id, configure.ReceiverBand.BAND_1, [fsp_config])
    request_1 = configure.ConfigureRequest(123, pointing_config, dish_config,csp_config)

    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    channel_avg_map = [(1, 2), (745, 0), (1489, 0), (2233, 0), (2977, 0), (3721, 0), (4465, 0),
                       (5209, 0), (5953, 0), (6697, 0), (7441, 0), (8185, 0), (8929, 0), (9673, 0), (10417, 0),
                       (11161, 0), (11905, 0), (12649, 0), (13393, 0), (14137, 0)]
    scan_id = 123
    fsp_config = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = configure.CSPConfiguration(scan_id, configure.ReceiverBand.BAND_1, [fsp_config])
    request_2 = configure.ConfigureRequest(123, pointing_config, dish_config, csp_config)

    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest is not equal to other objects.
    """
    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    channel_avg_map = [(1, 2), (745, 0), (1489, 0), (2233, 0), (2977, 0), (3721, 0), (4465, 0),
                       (5209, 0), (5953, 0), (6697, 0), (7441, 0), (8185, 0), (8929, 0), (9673, 0), (10417, 0),
                       (11161, 0), (11905, 0), (12649, 0), (13393, 0), (14137, 0)]
    scan_id = 123
    fsp_config = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = configure.CSPConfiguration(scan_id, configure.ReceiverBand.BAND_1, [fsp_config])
    request = configure.ConfigureRequest(123, pointing_config, dish_config, csp_config)

    assert request != object


def test_fsp_id_range():
    """
    verify that fsp id is in the range of 1 to 27
    :return:
    """
    fsp_id = 29
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(fsp_id, configure.FSPFunctionMode.CORR, 1, 1400, 0)
    fsp_id = -1
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(fsp_id, configure.FSPFunctionMode.CORR, 1, 1400, 0)


def test_fsp_slice_id_range():
    """
    verify that fsp slice id is in the range of 1 to 26
    :return:
    """

    fsp_slice_id = 36
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, fsp_slice_id, 1400, 0)

def test_corr_bandwidth_range():
    """
    verify that crr_bandwidth is in the range of 0 to 6
    :return:
    """
    corr_bandwidth = 7
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, corr_bandwidth)

def test_corr_bandwidth_range():
    """
    verify that crr_bandwidth is in the range of 0 to 6
    :return:
    """
    corr_bandwidth = 7
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, corr_bandwidth)


def test_corr_bandwidth_range():
    """
    Verify that integration time is multiple of 140
    """
    integration_time = 1401
    with pytest.raises(ValueError):
        _ = configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, integration_time, 0)

def test_number_of_channel_avg_mapping_tuples():
    """
    Verify that FSPConfiguration fails if there  < or > 20 tuples in chan avg mapping
    :return:
    """
    # test for 18 tuples
    channel_avg_map = [(745, 0), (1489, 0), (2233, 0), (2977, 0), (3721, 0), (4465, 0),
                      (5209, 0), (5953, 0), (6697, 0), (7441, 0), (8929, 0), (9673, 0), (10417, 0),
                      (11161, 0), (11905, 0), (12649, 0), (13393, 0), (14137, 0)]

    with pytest.raises(ValueError):
         _= configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)

     #test for 22 tuples
    channel_avg_map = [(1, 2), (745, 0), (1489, 0), (2233, 0), (2977, 0), (3721, 0), (4465, 0),
                       (5209, 0), (5953, 0), (6697, 0), (7441, 0), (8185, 0), (8929, 0), (9673, 0), (10417, 0),
                       (11161, 0), (11905, 0), (12649, 0), (13393, 0), (14137, 0), (14137, 1), (2, 3)]
    with pytest.raises(ValueError):
         _= configure.FSPConfiguration(1, configure.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)

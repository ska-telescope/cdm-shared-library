"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import ska.cdm.messages.subarray_node.configure as configure


def test_target_defaults():
    """
    Verify Target default arguments.
    """
    target_1 = configure.Target(ra=1, dec=0.5)
    target_2 = configure.Target(ra=1, dec=0.5, name='', frame='icrs', unit='rad')
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


def test_target_str():
    """
    Verify the string representation of a Target.
    """
    target = configure.Target(ra=1, dec=2, name='name', frame='icrs', unit='deg')
    expected = "<Target(ra=1.0, dec=2.0, name='name', frame='icrs', unit='deg')>"
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
    channel_avg_map = [[1, 2], [745, 0], [1489, 0], [2233, 0], [2977, 0], [3721, 0], [4465, 0],
                       [5209, 0], [5953, 0], [6697, 0], [7441, 0], [8185, 0], [8929, 0], [9673, 0], [10417, 0],
                       [11161, 0], [11905, 0], [12649, 0], [13393, 0], [14137, 0]]
    fsp_config = configure.FSPConfiguration("1","CORR", 1, 1400, 0, channel_avg_map)
    csp_config = configure.CSPConfiguration("1" ,fsp_config)
    request_1 = configure.ConfigureRequest(123, pointing_config, dish_config,csp_config)

    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    request_2 = configure.ConfigureRequest(123, pointing_config, dish_config, csp_config)

    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest is not equal to other objects.
    """
    pointing_config = configure.PointingConfiguration(configure.Target(1, 1))
    dish_config = configure.DishConfiguration(receiver_band=configure.ReceiverBand.BAND_1)
    channel_avg_map = [[1, 2], [745, 0], [1489, 0], [2233, 0], [2977, 0], [3721, 0], [4465, 0],
                       [5209, 0], [5953, 0], [6697, 0], [7441, 0], [8185, 0], [8929, 0], [9673, 0], [10417, 0],
                       [11161, 0], [11905, 0], [12649, 0], [13393, 0], [14137, 0]]
    fsp_config = configure.FSPConfiguration("1", "CORR", 1,
                                     1400, 0, channel_avg_map)
    csp_config = configure.CSPConfiguration("1", fsp_config)
    request = configure.ConfigureRequest(123, pointing_config, dish_config, csp_config)
    assert request != object

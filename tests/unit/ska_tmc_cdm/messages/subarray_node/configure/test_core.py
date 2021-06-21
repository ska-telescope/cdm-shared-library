"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.common module.
"""
from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    PointingConfiguration,
    ReceiverBand,
    Target,
)


def test_target_defaults():
    """
    Verify Target default arguments.
    """
    target_1 = Target(ra=1, dec=0.5)
    target_2 = Target(ra=1, dec=0.5, name="", frame="icrs", unit=("hourangle", "deg"))
    assert target_1 == target_2


def test_target_eq():
    """
    Verify that Target objects are considered equal when:

      - they have the same name
      - they point to the same place on the sky
      - they use the same co-ordinate frame
      - they use the same co-ordinate units
    """
    target_1 = Target(ra=1, dec=2, name="a source", frame="fk5", unit="deg")
    target_2 = Target(ra=1, dec=2, name="a source", frame="fk5", unit="deg")
    target_3 = Target(ra=1, dec=1)
    assert target_1 == target_2
    assert target_1 != target_3


def test_target_is_not_equal_to_other_objects():
    """
    Verify that Target objects are considered unequal to other objects.
    """
    target = Target(ra=1, dec=2, name="a source", frame="fk5", unit="deg")
    assert target != object


def test_target_repr():
    """
    Verify the repr representation of a Target.
    """
    target = Target(ra=30, dec=-3600, name="name", frame="icrs", unit=("deg", "arcsec"))
    expected = (
        "<Target(ra=30.0, dec=-1.0, name='name', frame='icrs', unit=('deg', 'deg'))>"
    )
    assert expected == repr(target)


def test_target_str():
    """
    Verify the string representation of a Target.
    """
    target = Target(ra=30, dec="0", name="name", frame="icrs", unit=("deg", "rad"))
    expected = "<Target: 'name' (02h00m00s +00d00m00s icrs)>"
    assert expected == str(target)


def test_pointing_configuration_eq():
    """
    Verify that PointingConfiguration objects are considered equal when:
      - they point to the same target
    """
    target_1 = Target(ra=1, dec=2, name="a source", frame="fk5", unit="deg")
    target_2 = Target(ra=1, dec=2, name="a source", frame="fk5", unit="deg")
    target_3 = Target(ra=1, dec=2, name="foobar", frame="fk4", unit="deg")
    config_1 = PointingConfiguration(target_1)
    config_2 = PointingConfiguration(target_2)
    config_3 = PointingConfiguration(target_3)
    assert config_1 == config_2
    assert config_1 != config_3


def test_pointing_configuration_is_not_equal_to_other_objects():
    """
    Verify that PointingConfiguration is not considered equal to
    non-PointingConfiguration objects.
    """
    target = Target(ra=1, dec=2, name="a source", frame="fk5", unit="deg")
    config = PointingConfiguration(target)
    assert config != object


def test_dish_configuration_eq():
    """
    Verify that DishConfiguration objects are considered equal when:
      - they use the same receiver band
    """
    config_1 = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    config_2 = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    config_3 = DishConfiguration(receiver_band=ReceiverBand.BAND_2)
    assert config_1 == config_2
    assert config_1 != config_3


def test_dish_configuration_is_not_equal_to_other_objects():
    """
    Verify that DishConfiguration is considered unequal to
    non-DishConfiguration objects.
    """
    config_1 = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    assert config_1 != Target(1, 1)
    assert config_1 != object

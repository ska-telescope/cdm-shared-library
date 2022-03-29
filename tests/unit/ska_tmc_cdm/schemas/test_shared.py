"""
Unit tests for the ska_tmc_cdm.schemas.shared module.
"""
import ska_tmc_cdm.schemas.shared as shared


def test_upper_cased_field_serialises_to_uppercase():
    """
    Verify that UpperCasedField serialises to uppercase text.
    """

    class TestObject:  # pylint: disable=too-few-public-methods
        """
        Simple test object to hold an attribute.
        """

        def __init__(self):
            self.attr = "bar"

    obj = TestObject()
    serialised = shared.UpperCasedField().serialize("attr", obj)
    assert serialised == "BAR"


def test_upper_cased_field_serialises_none():
    """
    Verify that UpperCasedField serialises None to an empty string.
    """

    class TestObject:  # pylint: disable=too-few-public-methods
        """
        Simple test object to hold an attribute.
        """

        def __init__(self):
            self.attr = None

    obj = TestObject()
    serialised = shared.UpperCasedField().serialize("attr", obj)
    assert serialised == ""


def test_upper_cased_field_deserialises_to_uppercase():
    """
    Verify that UpperCasedField deserialises to lowercase text.
    """
    deserialised = shared.UpperCasedField().deserialize("FOO")
    assert deserialised == "foo"

"""
The schemas module defines Marshmallow schemas that are shared by various
other serialisation schemas.
"""

from marshmallow import Schema
from marshmallow.fields import Field

__all__ = ['UpperCasedField', 'OrderedSchema']


class UpperCasedField(Field):  # pylint: disable=too-few-public-methods
    """
    Field that serializes to an upper-case string and deserializes
    to a lower-case string.
    """

    def _serialize(self, value, attr, obj, **kwargs):  # pylint: disable=no-self-use
        if value is None:
            return ''
        return value.upper()

    def _deserialize(self, value, attr, data, **kwargs):  # pylint: disable=no-self-use
        return value.lower()


class OrderedSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Subclass of Schema, anything inheriting from Schema  has the
    order of its JSON properties respected in the message. Saves adding
    a Meta class to everything individually
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        marshmallow directive to respect order of JSON properties  in message.
        """
        ordered = True

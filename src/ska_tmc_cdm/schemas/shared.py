"""
The schemas module defines Marshmallow schemas that are shared by various
other serialisation schemas.
"""

from marshmallow import Schema, post_dump, pre_load
from marshmallow.fields import Field

from ..jsonschema.json_schema import JsonSchema

__all__ = ["UpperCasedField", "OrderedSchema", "ValidatingSchema"]


class UpperCasedField(Field):  # pylint: disable=too-few-public-methods
    """
    Field that serializes to an upper-case string and deserializes
    to a lower-case string.
    """

    def _serialize(self, value, attr, obj, **kwargs):  # pylint: disable=no-self-use
        if value is None:
            return ""
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


class ValidatingSchema(Schema):
    """
    ValidatingSchema is a marshmallow schema that calls the appropriate
    Telescope Model schema validation functions when serialising or
    deserialising  JSON.
    """

    # Marshmallow context key that holds Telescope Model validation toggle
    VALIDATE = "Run TM validation"
    # Marshmallow context key that holds Telescope Model strictness level
    VALIDATION_STRICTNESS = "TM schema strictness"

    SEMANTIC_VALIDATE = "Run Semantic validation"

    @pre_load
    def validate_on_load(self, data, process_fn=lambda x: x, **_):
        """
        Validate the JSON string to deserialise.

        :param data: Marshmallow-provided dict containing parsed object values
        :param process_fn: function to process data before validation
        :param _: unused kwargs passed by Marshmallow
        :return: dict suitable for object constructor.
        """
        self.validate_json(data, process_fn=process_fn)
        self.semantic_validate_json(dict(data))
        return data

    @post_dump
    def validate_on_dump(
        self, data, process_fn=lambda x: x, **_
    ):  # pylint: disable=no-self-use
        """
        Validate the serialised object against the relevant Telescope Model
        schema.

        :param data: Marshmallow-provided dict containing parsed object values
        :param process_fn: function to process data before validation
        :param _: unused kwargs passed by Marshmallow
        :return: dict suitable for writing as a JSON string
        """
        self.validate_json(data, process_fn=process_fn)
        self.semantic_validate_json(dict(data))
        return data

    def validate_json(self, data, process_fn):
        """
        Validate JSON using the Telescope Model schema.

        The process_fn argument can be used to process semantically correct
        but schematically invalid Python to something equivalent but valid,
        e.g., to convert a list of Python tuples to a list of lists.

        :param data: Marshmallow-provided dict containing parsed object values
        :param process_fn: data processing function called before validation
        :return:
        """
        validate = self.context.get(self.VALIDATE, False)
        if not validate:
            return

        strictness = self.context.get(self.VALIDATION_STRICTNESS, None)
        interface = data.get("interface", None)
        if interface:
            JsonSchema.validate_schema(
                interface, process_fn(data), strictness=strictness
            )

    def semantic_validate_json(self, data, process_fn=lambda x: x, **_):
        validate = self.context.get(self.SEMANTIC_VALIDATE, False)
        if not validate:
            return
        interface = data.get("interface", None)
        JsonSchema.semantic_validate_schema(process_fn(data), interface)

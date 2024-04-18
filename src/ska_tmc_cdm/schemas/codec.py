"""
The codec module contains classes used by clients to marshall CDM classes to
and from JSON. This saves the clients having to instantiate and manipulate the
Marshmallow schema directly.
"""
__all__ = ["MarshmallowCodec"]

from typing import Optional

from .shared import ValidatingSchema

STRICTNESS = None


class MarshmallowCodec:  # pylint: disable=too-few-public-methods
    """
    MarshmallowCodec marshalls and unmarshalls CDM classes.

    The mapping of CDM classes to Marshmallow schema is defined in this class.
    """

    def __init__(self):
        self._schema = {}

    def register_mapping(self, cdm_class):
        """A decorator that is used to register the mapping between a
        Marshmallow schema and the CDM class it serialises.

        :param cdm_class: the CDM class this schema maps to
        :return: the decorator
        """

        def decorator(class_definition):
            self.set_schema(cdm_class, class_definition)
            return class_definition

        return decorator

    def set_schema(self, cdm_class, schema_class):
        """
        Set the schema for a CDM class.

        :param schema_class: Marshmallow schema to map
        :param cdm_class: CDM class the schema maps to
        """

        self._schema[cdm_class] = schema_class

    def load_from_file(
        self,
        cls,
        path,
        validate: bool = True,
        strictness: Optional[int] = STRICTNESS,
    ):
        """
        Load an instance of a CDM class from disk.

        :param cls: the class to create from the file
        :param path: the path to the file
        :param validate: True to enable schema validation
        :param strictness: optional validation strictness level (0=min, 2=max)
        :return: an instance of cls
        """
        with open(path, "r", encoding="utf-8") as json_file:
            json_data = json_file.read()
            return self.loads(cls, json_data, validate, strictness)

    def loads(
        self,
        cdm_class,
        json_data,
        validate: bool = True,
        strictness: Optional[int] = STRICTNESS,
    ):
        """
        Create an instance of a CDM class from a JSON string.

        The default strictness of the Telescope Model schema validator can be
        overridden by supplying the validate argument.

        :param cdm_class: the class to create from the JSON
        :param json_data: the JSON to unmarshall
        :param validate: True to enable schema validation
        :param strictness: optional validation strictness level (0=min, 2=max)
        :return: an instance of cls
        """
        schema_cls = self._schema[cdm_class]
        schema_obj = schema_cls()

        schema_obj.context[ValidatingSchema.VALIDATE] = validate
        if strictness is not None:
            schema_obj.context[
                ValidatingSchema.VALIDATION_STRICTNESS
            ] = strictness

        return schema_obj.loads(json_data=json_data)

    def dumps(
        self,
        obj,
        validate: bool = True,
        strictness: Optional[int] = STRICTNESS,
    ):
        """
        Return a string JSON representation of a CDM instance.

        The default strictness of the Telescope Model schema validator can be
        overridden by supplying the validate argument.

        :param obj: the instance to marshall to JSON
        :param validate: True to enable schema validation
        :param strictness: optional validation strictness level (0=min, 2=max)
        :return: JSON representation of obj
        """
        schema_cls = self._schema[obj.__class__]
        schema_obj = schema_cls()

        schema_obj.context[ValidatingSchema.VALIDATE] = validate
        if strictness is not None:
            schema_obj.context[
                ValidatingSchema.VALIDATION_STRICTNESS
            ] = strictness

        return schema_obj.dumps(obj)

"""
The codec module contains classes used by clients to marshall CDM classes to
and from JSON. This saves the clients having to instantiate and manipulate the
Marshmallow schema directly.
"""
import json
from ska.cdm.jsonschema.json_schema import JsonSchema

__all__ = ['MarshmallowCodec']


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

    def load_from_file(self, cls, path, validation_required: bool = True):
        """
        Load an instance of a CDM class from disk.

        :param cls: the class to create from the file
        :param path: the path to the file
        :param validation_required: default value set to true for schema
               validation
        :return: an instance of cls
        """

        with open(path, 'r') as json_file:
            json_data = json_file.read()
            if validation_required:
                MarshmallowCodec.call_to_validate(json_data)
            return self.loads(cls, json_data)

    def loads(self, cdm_class, json_data, validation_required: bool = True):
        """
        Create an instance of a CDM class from a JSON string.

        :param cdm_class: the class to create from the JSON
        :param json_data: the JSON to unmarshall
        :param validation_required: default value set to true for schema
               validation
        :return: an instance of cls
        """

        schema_cls = self._schema[cdm_class]
        schema_obj = schema_cls()
        if validation_required:
            MarshmallowCodec.call_to_validate(json_data)
        return schema_obj.loads(json_data=json_data)

    def dumps(self, obj, validation_required: bool = True):
        """
        Return a string JSON representation of a CDM instance.

        :param obj: the instance to marshall to JSON
        :param validation_required: default value set to true for schema
               validation
        :return: a JSON string
        """

        schema_cls = self._schema[obj.__class__]
        schema_obj = schema_cls()
        if validation_required:
            MarshmallowCodec.call_to_validate(schema_obj.dumps(obj))
        return schema_obj.dumps(obj)

    @staticmethod
    def call_to_validate(json_data: str):
        """
        Use for CSP schema validation

        :param json_data: the instance to marshall to JSON
        """

        json_dict = json.loads(json_data)
        if ('csp' in json_dict and json_dict['csp']) and \
                ('interface' in json_dict['csp'] and json_dict['csp']['interface']):
            JsonSchema.validate_schema(json_dict['csp']['interface'], json_dict['csp'])
        elif 'interface' in json_dict and json_dict['interface']:
            JsonSchema.validate_schema(json_dict['interface'], json_dict)

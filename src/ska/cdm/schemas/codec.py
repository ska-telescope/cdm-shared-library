"""
The codec module contains classes used by clients to marshall CDM classes to
and from JSON. This saves the clients having to instantiate and manipulate the
Marshmallow schema directly.
"""
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

    def load_from_file(self, cls, path, validate: bool = True):
        """
        Load an instance of a CDM class from disk.

        :param cls: the class to create from the file
        :param path: the path to the file
        :param validate: default value set to true for schema
               validation
        :return: an instance of cls
        """

        with open(path, 'r') as json_file:
            json_data = json_file.read()
            return self.loads(cls, json_data, validate)

    def loads(self, cdm_class, json_data, validate: bool = True):
        """
        Create an instance of a CDM class from a JSON string.

        :param cdm_class: the class to create from the JSON
        :param json_data: the JSON to unmarshall
        :param validate: default value set to true for schema
               validation
        :return: an instance of cls
        """

        schema_cls = self._schema[cdm_class]
        schema_obj = schema_cls()
        # schema_obj.context["custom_validate"] = validate
        return schema_obj.loads(json_data=json_data)

    def dumps(self, obj, validate: bool = True):
        """
        Return a string JSON representation of a CDM instance.

        :param obj: the instance to marshall to JSON
        :param validate: default value set to true for schema
               validation
        :return: a JSON string
        """

        schema_cls = self._schema[obj.__class__]
        schema_obj = schema_cls()
        # schema_obj.context["custom_validate"] = validate
        return schema_obj.dumps(obj)

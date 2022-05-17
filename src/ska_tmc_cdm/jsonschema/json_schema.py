"""
The JSON Schema module contains methods for fetching version-specific JSON schemas
using interface uri and validating the structure of JSON against these schemas.
"""

from ska_telmodel import schema

from ska_tmc_cdm.exceptions import JsonValidationError, SchemaNotFound

__all__ = ["JsonSchema"]


class JsonSchema:  # pylint: disable=too-few-public-methods
    """
    JSON Schema use for validating the structure of JSON data
    """

    @staticmethod
    def get_schema_by_uri(uri: str) -> schema.Schema:
        """
        Retrieve JSON Schemas from remote server.

        :param uri: Interface Version URI
        :return: Interface schema
        :raises: SchemaNotFound if URI does not resolve to a schema
        """
        try:
            return schema.schema_by_uri(uri)
        except ValueError as exc:
            raise SchemaNotFound(uri) from exc

    @staticmethod
    def validate_schema(uri: str, instance: dict, strictness=None) -> None:
        """
        Validate an instance dictionary under the given schema.

        strictness can be set from 0-2. Values equal:

          0: permissive warnings
          1: permissive errors and strict warnings
          2: strict errors

        :param uri:  The schema to validate with
        :param instance: The instance to validate
        :param strictness: strictness level
        :return: None, in case of valid data otherwise, it raises an exception.
        """
        # use default strictness defined by Telescope Model unless overridden
        extra_kwargs = {}
        if strictness is not None:
            extra_kwargs["strictness"] = strictness

        try:
            return schema.validate(uri, instance, **extra_kwargs)
        except ValueError as exc:
            # Distinguish ValueErrors caused by schema not found from
            # ValueErrors caused by invalid JSON.
            try:
                schema.schema_by_uri(uri)
            except ValueError:
                if strictness is not None and strictness > 1:
                    raise SchemaNotFound(uri) from exc
            else:
                raise JsonValidationError(uri, instance) from exc

"""
The JSON Schema module contains methods for fetching version-specific JSON schemas
using interface uri and validating the structure of JSON against these schemas.
"""

from ska_telmodel import schema
from ska.cdm.exceptions import JsonValidationError

__all__ = ['JsonSchema']


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
        """
        try:
            return schema.schema_by_uri(uri)
        except ValueError as exc:
            raise JsonValidationError(uri) from exc

    @staticmethod
    def validate_schema(uri: str, instance: dict):
        """
        Validate an instance dictionary under the given schema.

        :param uri:  The schema to validate with
        :param instance: The instance to validate
        :return: None, in case of valid data otherwise, it raises an exception.
        """
        try:
            return schema.validate(uri, instance)
        except ValueError as exc:
            raise JsonValidationError(uri, instance) from exc

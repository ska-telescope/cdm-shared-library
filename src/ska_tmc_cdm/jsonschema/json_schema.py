"""
The JSON Schema module contains methods for fetching version-specific JSON schemas
using interface uri and validating the structure of JSON against these schemas.
"""
import warnings
from enum import Enum
from importlib.metadata import version
from os import environ

from ska_ost_osd.telvalidation import (
    semantic_validator as televalidation_schema,
)
from ska_ost_osd.telvalidation.semantic_validator import (
    SchematicValidationError,
)
from ska_telmodel import schema
from ska_telmodel.data import TMData

from ska_tmc_cdm.exceptions import JsonValidationError, SchemaNotFound

__all__ = ["JsonSchema"]

# SKA OSD data is not packaged with the client library, and by default the library will fetch the "latest"
# version in git, which may contain unreleased, breaking changes. We want to explicitly pin to the same data
# version as the library version:

OSD_LIB_VERSION = version("ska_ost_osd")
CAR_OSD_SOURCE = (f"car:ost/ska-ost-osd?{OSD_LIB_VERSION}#tmdata",)


class ValidationLevel(Enum):
    # fmt: off
    PERMISSIVE  = -9 # Only builtin pydantic validation, don't call any external validation libraries.
    AGNOSTIC    = -1 # Express no opinion on validation, OSD and telmodel decide what to do.
    BASIC_WARN  =  0 # Runs only basic validations and log warnings, not errors ('permissive warnings' in telmodel)
    BASIC_ERROR =  1 # Run all OSD validations ('permissive', 'strict' and 'semantic') but only raise errors for basic syntax failures.
    ALL_ERROR   =  2 # Run all validations, raise exceptions and refuse to process invalid documents.
    # fmt: on


class JsonSchema:
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
    def validate_schema(
        uri: str,
        instance: dict,
        strictness: ValidationLevel = ValidationLevel.AGNOSTIC,
    ) -> None:
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
        extra_kwargs = {}
        # Only pass strictness parameter if caller
        # has asked for something:
        if strictness > ValidationLevel.AGNOSTIC:
            extra_kwargs["strictness"] = strictness.value

        try:
            return schema.validate(uri, instance, **extra_kwargs)
        except ValueError as exc:
            _check_for_missing_schema(exc, uri, strictness)
            # Distinguish ValueErrors caused by schema not found from
            # ValueErrors caused by invalid JSON.
            raise JsonValidationError(exc, uri, instance) from exc

    @classmethod
    def semantic_validate_schema(
        instance: dict,
        uri: str,
        strictness: ValidationLevel = ValidationLevel.AGNOSTIC,
    ) -> None:
        """
        Validate an instance dictionary under the given schema.

        :param uri:  The schema to validate with
        :param instance: The instance to validate
        :return: None, in case of valid data otherwise, it raises an exception.
        """

        if env_var_sources := environ.get("SKA_TELMODEL_SOURCES"):
            data_sources = env_var_sources.split(",")
        else:
            data_sources = CAR_OSD_SOURCE

        tm_data = TMData(source_uris=data_sources, update=True)
        try:
            return televalidation_schema.semantic_validate(
                observing_command_input=instance,
                tm_data=tm_data,
                interface=uri,
            )
        except SchematicValidationError as exc:
            _check_for_missing_schema(exc, uri, strictness)
            if strictness >= ValidationLevel.EXCEPTIONS:
                raise
            else:
                warnings.warn(exc)


def _check_for_missing_schema(
    original_error: SchematicValidationError,
    uri: str,
    strictness: ValidationLevel,
):
    """
    OSD Telvalidation raises a standard SchematicValidationError for all
    issues, but we want to distinguish missing schemas from failed validation.
    """
    # TODO: This could be made cleaner by having OSD raise a more specific
    # subclass of exception for missing schemas.
    try:
        JsonSchema.get_schema_by_uri(uri)
    except SchemaNotFound as notfound:
        if strictness >= 1:
            raise notfound from original_error
        elif strictness == ValidationLevel.WARNING:
            warnings.warn(notfound)

"""
The exceptions module contains all custom exceptions that are
part of the CDM library.
"""

from ska_telmodel.telvalidation.semantic_validator import (
    SchematicValidationError,
)


class JsonValidationError(ValueError):
    """
    Error raised when schema does not match with the SKA
    schema version.
    """

    def __init__(
        self, exc: SchematicValidationError, uri: str, json_dict: dict = None
    ):
        self._msg = f"JSON validation error: {exc}"
        super().__init__(self._msg)
        self.exc = exc
        self.uri = uri
        self.json_dict = json_dict

    def __str__(self):
        return f"{self._msg}"


class SchemaNotFound(ValueError):
    """
    Error raised when schema cannot be found.
    """

    def __init__(self, uri: str):
        self._msg = f"JSON schema not found: {uri}"
        super().__init__(self._msg)
        self.uri = uri

    def __str__(self):
        return f"{self._msg}"

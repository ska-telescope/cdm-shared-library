"""
The exceptions module contains all custom exceptions that are
part of the CDM library.
"""


class JsonValidationError(ValueError):
    """
    Error raised when schema does not match with the SKA
    schema version.
    """

    def __init__(self, uri: str, json_dict: dict = None):
        self._msg = f'JSON validation error: data is not compliant with {uri}'
        super().__init__(self._msg)
        self.uri = uri
        self.json_dict = json_dict

    def __str__(self):
        return f'{self._msg}'

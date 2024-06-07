"""
The codec module contains classes used by clients to marshall CDM classes to
and from JSON. This saves the clients having to instantiate and manipulate the
Marshmallow schema directly.
"""
__all__ = ["Codec"]

from os import PathLike

from typing import Optional, Type

from .shared import ValidatingSchema

STRICTNESS = None

class Codec:

    @staticmethod
    def loads(
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
        return cdm_class.model_validate_json(json_data)

    @staticmethod
    def dumps(
        obj,
        validate: bool = True,
        strictness: Optional[int] = STRICTNESS,
    ) -> str:
        """
        Return a string JSON representation of a CDM instance.

        The default strictness of the Telescope Model schema validator can be
        overridden by supplying the validate argument.

        :param obj: the instance to marshall to JSON
        :param validate: True to enable schema validation
        :param strictness: optional validation strictness level (0=min, 2=max)
        :return: JSON representation of obj
        """
        return obj.model_dump_json(exclude_none=True)

    @staticmethod
    def load_from_file(
        cdm_class: Type[Cdm],
        path: PathLike[str],
        validate: bool = True,
        strictness: Optional[int] = STRICTNESS,
    ):
        """
        Load an instance of a CDM class from disk.

        :param cdm_class: the class to create from the file
        :param path: the path to the file
        :param validate: True to enable schema validation
        :param strictness: optional validation strictness level (0=min, 2=max)
        :return: an instance of cls
        """
        with open(path, "r", encoding="utf-8") as json_file:
            json_data = json_file.read()
            return Codec.loads(cdm_class, json_data, validate, strictness)
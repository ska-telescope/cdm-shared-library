"""
The codec module contains classes used by clients to marshall CDM classes to
and from JSON. This saves the clients having to instantiate and manipulate the
Marshmallow schema directly.
"""
__all__ = ["Codec"]

import json
from os import PathLike
from typing import Optional, Type

from ska_tmc_cdm.messages.base import CdmObject

from .telmodel_validation import semantic_validate_json, validate_json

DEFAULT_STRICTNESS = 0


class Codec:
    @staticmethod
    def _telmodel_validation(enforced: bool, jsonable_data: dict, strictness: int = 0):
        if not enforced:
            return
        validate_json(jsonable_data, strictness=strictness)
        semantic_validate_json(jsonable_data)

    @staticmethod
    def loads(
        cdm_class: Type[CdmObject],
        json_data: str,
        validate: bool = True,
        strictness: int = DEFAULT_STRICTNESS,
    ) -> CdmObject:
        """
        Create an instance of a CDM class from a JSON string.

        The default strictness of the Telescope Model schema validator can be
        overridden by supplying the validate argument.

        :param cdm_class: the class to create from the JSON
        :param json_data: the JSON to unmarshall
        :param validate: True to enable schema validation
        :param strictness: optional validation strictness level (0=min, 2=max)
        :return: an instance of CdmObject
        """
        # Making Pydantic the first line of validation gives us
        # basic checks up front, and also yields performance benefits
        # because it uses a fast Rust JSON parser internally.
        obj = cdm_class.model_validate_json(json_data)
        jsonable_dict = obj.model_dump(exclude_none=True, by_alias=True)
        Codec._telmodel_validation(validate, jsonable_dict, strictness)
        return obj

    @staticmethod
    def dumps(
        obj: CdmObject,
        validate: bool = True,
        strictness: int = DEFAULT_STRICTNESS,
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
        jsonable_dict = obj.model_dump(exclude_none=True, by_alias=True)
        Codec._telmodel_validation(validate, jsonable_dict, strictness)
        return json.dumps(jsonable_dict)

    @staticmethod
    def load_from_file(
        cdm_class: Type[CdmObject],
        path: PathLike[str],
        validate: bool = True,
        strictness: Optional[int] = DEFAULT_STRICTNESS,
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

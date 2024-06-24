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

from .telmodel_validation import (
    ValidationLevel,
    semantic_validate_json,
    validate_json,
)


class Codec:
    @staticmethod
    def _telmodel_validation(
        jsonable_data: dict,
        strictness: ValidationLevel = ValidationLevel.AGNOSTIC,
    ):
        if strictness <= ValidationLevel.PERMISSIVE:
            pass
        elif strictness == ValidationLevel.AGNOSTIC:
            # Run everything, it's up to OSD/Telmodel what to do:
            validate_json(jsonable_data, strictness=strictness)
            semantic_validate_json(jsonable_data)
        elif strictness == ValidationLevel.BASIC_WARN:
            validate_json(jsonable_data, strictness=strictness)
        elif strictness >= ValidationLevel.BASIC_ERROR:
            validate_json(jsonable_data, strictness=strictness)
            semantic_validate_json(jsonable_data, strictness=strictness)
        else:
            raise ValueError(f"Ambiguous validation strictness: {strictness}")

    @staticmethod
    def loads(
        cdm_class: Type[CdmObject],
        json_data: str,
        strictness: ValidationLevel = ValidationLevel.AGNOSTIC,
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
        jsonable_dict = obj.model_dump(
            mode="json", exclude_none=True, by_alias=True
        )
        Codec._telmodel_validation(validate, jsonable_dict, strictness)
        return obj

    @staticmethod
    def dumps(
        obj: CdmObject,
        strictness: ValidationLevel = ValidationLevel.AGNOSTIC,
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
        jsonable_dict = obj.model_dump(
            mode="json", exclude_none=True, by_alias=True
        )
        Codec._telmodel_validation(jsonable_dict, strictness)
        return json.dumps(jsonable_dict)

    @staticmethod
    def load_from_file(
        cdm_class: Type[CdmObject],
        path: PathLike[str],
        strictness: Optional[int] = ValidationLevel.AGNOSTIC,
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
            return Codec.loads(cdm_class, json_data, strictness)

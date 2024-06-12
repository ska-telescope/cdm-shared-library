"""
The codec module contains classes used by clients to marshall CDM classes to
and from JSON. This saves the clients having to instantiate and manipulate the
Marshmallow schema directly.
"""
__all__ = ["Codec"]

from os import PathLike
from typing import Optional, Type
from ..jsonschema.json_schema import JsonSchema


from ska_tmc_cdm.messages.base import CdmObject

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
        return obj.model_dump_json(exclude_none=True, by_alias=True)

    @staticmethod
    def load_from_file(
        cdm_class: Type[CdmObject],
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


    @staticmethod
    def semantic_validate_json(data, process_fn=lambda x: x, **_):
        """
        Validate JSON using the Telescope Model schema.

        The process_fn argument can be used to process semantically correct
        but schematically invalid Python to something equivalent but valid,
        e.g., to convert a list of Python tuples to a list of lists.

        :param data: Marshmallow-provided dict containing parsed object values
        :param process_fn: data processing function called before validation
        :return:
        """
        interface = data.get("interface", None)
        # TODO: This fails 'open' instead of failing 'closed', if the
        # caller is requesting strict validation and we can't even tell
        # what interface to validate against, that should be an error.
        if interface and (
            "ska-tmc-assignresources" in interface
            or "ska-tmc-configure" in interface
            or "ska-low-tmc-assignresources" in interface
            or "ska-low-tmc-configure" in interface
        ):
            JsonSchema.semantic_validate_schema(process_fn(data), interface)

"""
The schemas module defines Marshmallow schemas that are shared by various
other serialisation schemas.
"""

from typing import Callable, Optional

from ..jsonschema.json_schema import JsonSchema


def _identity(x):
    return x


def validate_json(
    data: dict,
    process_fn: Callable = _identity,
    strictness: Optional[int] = None,
):
    """
    Validate JSON using the Telescope Model schema.

    The process_fn argument can be used to process semantically correct
    but schematically invalid Python to something equivalent but valid,
    e.g., to convert a list of Python tuples to a list of lists.

    :param data: Dict containing parsed object values
    :param process_fn: data processing function called before validation
    :return:
    """

    interface = data.get("interface", None)
    # TODO: This fails 'open' instead of failing 'closed', if the
    # caller is requesting strict validation and we can't even tell
    # what interface to validate against, that should be an error.
    if interface:
        JsonSchema.validate_schema(
            interface, process_fn(data), strictness=strictness
        )


def semantic_validate_json(data, process_fn=_identity, **_):
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
        # These magic srings seem dodgy. Can we re/move them?
        "ska-tmc-assignresources" in interface
        or "ska-tmc-configure" in interface
        or "ska-low-tmc-assignresources" in interface
        or "ska-low-tmc-configure" in interface
    ):
        JsonSchema.semantic_validate_schema(process_fn(data), interface)

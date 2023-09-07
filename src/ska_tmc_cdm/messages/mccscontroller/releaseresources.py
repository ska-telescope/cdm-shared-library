"""
The allocate module defines a Python object model for the structured JSON that
forms the argument for an MCCSController.ReleaseResources  call.
"""
from dataclasses import KW_ONLY

from pydantic.dataclasses import dataclass

SCHEMA = "https://schema.skao.int/ska-low-mccs-releaseresources/2.0"


@dataclass
class ReleaseResourcesRequest:
    """
    ReleaseResourcesRequest is the object representation of the JSON argument
    for an MCCSController.ReleaseResources command.
    """

    _: KW_ONLY
    interface: str = SCHEMA
    subarray_id: int
    release_all: bool

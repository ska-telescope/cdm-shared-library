"""
The allocate module defines a Python object model for the structured JSON that
forms the argument for an MCCSController.ReleaseResources  call.
"""
from pydantic.dataclasses import dataclass

SCHEMA = "https://schema.skao.int/ska-low-mccs-releaseresources/2.0"


from ska_tmc_cdm.messages.base import CdmObject


class ReleaseResourcesRequest(CdmObject):
    """
    ReleaseResourcesRequest is the object representation of the JSON argument
    for an MCCSController.ReleaseResources command.
    """

    interface: str = SCHEMA
    subarray_id: int
    release_all: bool

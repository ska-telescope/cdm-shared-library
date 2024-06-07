"""
The allocate module defines a Python object model for the structured JSON
given in an MCCSController.Allocate call.
"""
from typing import Optional

from pydantic import Field

from ska_tmc_cdm.messages.base import CdmObject

__all__ = ["AllocateRequest"]

SCHEMA = "https://schema.skao.int/ska-low-mccs-assignresources/2.0"


class AllocateRequest(CdmObject):
    """
    AssignResourcesRequest is the object representation of the JSON argument
    for an MCCSController.Allocate command.

    :param subarray_id: the numeric SubArray ID
    :param subarray_beam_ids: subarray beam IDs to allocate to the subarray
    :param station_ids: IDs of stations to allocate
    :param channel_blocks: channels to allocate
    :param interface: the JSON schema this object claims to be compliant with
    """

    interface: Optional[str] = SCHEMA
    subarray_id: int
    subarray_beam_ids: list[int] = Field(default_factory=list)
    station_ids: list[list[int]] = Field(default_factory=list)
    channel_blocks: list[int] = Field(default_factory=list)

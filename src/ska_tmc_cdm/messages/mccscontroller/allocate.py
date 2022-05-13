"""
The allocate module defines a Python object model for the structured JSON
given in an MCCSController.Allocate call.
"""
from typing import List, Optional

__all__ = ["AllocateRequest"]

SCHEMA = "https://schema.skao.int/ska-low-mccs-assignresources/2.0"


class AllocateRequest:
    """
    AssignResourcesRequest is the object representation of the JSON argument
    for an MCCSController.Allocate command.
    """

    def __init__(
        self,
        *,  # force kwonly args
        interface: Optional[str] = SCHEMA,
        subarray_id: int,
        subarray_beam_ids: List[int] = None,
        station_ids: List[List[int]] = None,
        channel_blocks: List[int] = None,
    ):
        """
        Create a new request object for an MCCSController.Allocate command.

        :param subarray_id: the numeric SubArray ID
        :param subarray_beam_ids: subarray beam IDs to allocate to the subarray
        :param station_ids: IDs of stations to allocate
        :param channel_blocks: channels to allocate
        :param interface: the JSON schema this object claims to be compliant with
        """
        if subarray_beam_ids is None:
            subarray_beam_ids = []
        if station_ids is None:
            station_ids = []
        if channel_blocks is None:
            channel_blocks = []

        self.interface = interface
        self.subarray_id = subarray_id
        self.subarray_beam_ids = subarray_beam_ids
        self.station_ids = station_ids
        self.channel_blocks = channel_blocks

    def __eq__(self, other):
        """
        Check for equality between two AllocateRequest objects.

        :param other: the object to compare to this object
        :return: returns True if the objects are equal, else False
        """
        if not isinstance(other, AllocateRequest):
            return False
        return (
            self.interface == other.interface
            and self.subarray_id == other.subarray_id
            and self.subarray_beam_ids == other.subarray_beam_ids
            and self.station_ids == other.station_ids
            and self.channel_blocks == other.channel_blocks
        )

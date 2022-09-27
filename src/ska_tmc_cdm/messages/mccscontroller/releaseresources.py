"""
The allocate module defines a Python object model for the structured JSON that
forms the argument for an MCCSController.ReleaseResources  call.
"""
from typing import List, Optional

SCHEMA = "https://schema.skao.int/ska-low-mccs-releaseresources/2.0"


class ReleaseResourcesRequest:
    """
    ReleaseResourcesRequest is the object representation of the JSON argument
    for an MCCSController.ReleaseResources command.
     # two new addational parameters added for expand JSON schema
        :param subarray_beam_ids: subarray beam IDs to allocate to the subarray
        :param channels: channels to allocate
    """

    def __init__(
        self,
        *,  # force kwonly args
        interface: Optional[str] = SCHEMA,
        subarray_id: int,
        release_all: bool,
        subarray_beam_ids: List[int] = None,
        channels: List[List[int]] = None,
    ):

        # if subarray_beam_ids is None:
        #     self.subarray_beam_ids = None
        # if channels is None:
        #     self.channels = None

        self.interface = interface
        self.subarray_id = subarray_id
        self.release_all = release_all
        self.subarray_beam_ids = subarray_beam_ids
        self.channels = channels

    def __eq__(self, other):
        """
        Check for equality between two ReleaseResourcesRequest objects

        :param other: the object to compare to this object
        :return: True if the objects are the same, else False
        """
        if not isinstance(other, ReleaseResourcesRequest):
            return False
        return (
            self.interface == other.interface
            and self.subarray_id == other.subarray_id
            and self.release_all == other.release_all
            and self.subarray_beam_ids == other.subarray_beam_ids
            and self.channels == other.channels
        )

"""
TMC Assigned Resources
"""

from typing import List, Optional

__all__ = [
    "MCCSAllocation",
    "AssignedResources"
]

SCHEMA = "https://schema.skatelescope.org/ska-low-tmc-assignedresources/1.0"


class MCCSAllocation:
    """
    MCCSAllocation is a Python representation of the structured JSON
    representing the resources assigned to an MCCS subarray.
    """

    def __init__(
        self,
        subarray_beam_ids: List[int],
        station_ids: List[List[int]],
        channel_blocks: List[int],
    ):
        """
        Create a new Subarray object.

        :param subarray_beam_ids: the lisdt of SubArray Beam IDs
        :type subarray_beam_ids: List[int]
        :param station_ids: stations id's to MCCSAllocation
        :type station_ids: List[int]
        :param channel_blocks: channel_blocks
        :type channel_blocks: List[int]
        """
        self.subarray_beam_ids = subarray_beam_ids
        self.station_ids = list(station_ids)
        self.channel_blocks = list(channel_blocks)

    def __eq__(self, other):
        """
        Check for equality between two MCCSAllocation objects

        :param other: the object to check against this MCCSAllocation object
        :type other: MCCSAllocation object

        :return: returns True if the objects are the same, else False
        :rtype: boolean
        """
        if not isinstance(other, MCCSAllocation):
            return False
        return (
            self.subarray_beam_ids == other.subarray_beam_ids
            and self.station_ids == other.station_ids
            and self.channel_blocks == other.channel_blocks
        )

    def is_empty(self):
        """
        Determine that the current MCCSAllocation instance
        is empty (none of the attribute Lists are populated)
        """
        return not (
            self.subarray_beam_ids
            or self.station_ids
            or self.channel_blocks
        )

    def has_subarray_beam_ids(self):
        """
        Determines whether the subarray_beam_ids attribute
        is empty
        """
        return bool(self.subarray_beam_ids)

    def has_station_ids(self):
        """
        Determines whether the subarray_beam_ids attribute
        is empty
        """
        return bool(self.station_ids)

    def has_channel_blocks(self):
        """
        Determines whether the subarray_beam_ids attribute
        is empty
        """
        return bool(self.channel_blocks)


class AssignedResources:
    """
    AssignedResources models the structured JSON returned when the
    MCCSSubarray.assigned_resources Tango attribute is read.
    """
    def __init__(
        self,
        *,  # force kwargs
        interface: Optional[str] = SCHEMA,
        mccs: MCCSAllocation
    ):
        """
        Create a new AssignedResources instance.

        :param interface: JSON schema this instance conforms to
        :param mccs: the MCCSAllocation describing the allocated resources
        """
        self.interface = interface
        self.mccs = mccs

    def __eq__(self, other):
        if not isinstance(other, AssignedResources):
            return False
        return (
            self.mccs == other.mccs
            and self.interface == other.interface
        )

    def is_empty(self) -> bool:
        """
        Determine that the current MCCSAllocation instance
        is empty (none of the attribute Lists are populated)
        """
        return self.mccs.is_empty()

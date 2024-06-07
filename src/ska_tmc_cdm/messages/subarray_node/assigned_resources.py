"""
TMC Assigned Resources
"""

from typing import Optional

from pydantic.dataclasses import dataclass

__all__ = ["MCCSAllocation", "AssignedResources"]

SCHEMA = "https://schema.skao.int/ska-low-tmc-assignedresources/2.0"


from ska_tmc_cdm.messages.base import CdmObject


class MCCSAllocation(CdmObject):
    """
    MCCSAllocation is a Python representation of the structured JSON
    representing the resources assigned to an MCCS subarray.

    :param subarray_beam_ids: the lisdt of SubArray Beam IDs
    :type subarray_beam_ids: List[int]
    :param station_ids: stations id's to MCCSAllocation
    :type station_ids: List[int]
    :param channel_blocks: channel_blocks
    :type channel_blocks: List[int]
    """

    subarray_beam_ids: list[int]
    station_ids: list[list[int]]
    channel_blocks: list[int]

    def is_empty(self) -> bool:
        """
        Determine that the current MCCSAllocation instance
        is empty (none of the attribute Lists are populated)
        """
        return not (self.subarray_beam_ids or self.station_ids or self.channel_blocks)


from ska_tmc_cdm.messages.base import CdmObject


class AssignedResources(CdmObject):
    """
    AssignedResources models the structured JSON returned when the
    MCCSSubarray.assigned_resources Tango attribute is read.

    :param interface: JSON schema this instance conforms to, defaults to
        https://schema.skao.int/ska-low-tmc-assignedresources/2.0 if not set
    :param mccs: the MCCSAllocation describing the allocated resources
    """

    interface: Optional[str] = SCHEMA
    mccs: MCCSAllocation

    def is_empty(self) -> bool:
        """
        Determine that the current MCCSAllocation instance
        is empty (none of the attribute Lists are populated)
        """
        return self.mccs.is_empty()

# -*- coding: utf-8 -*-
#
# This file is part of the CDM library
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

from typing import List, Optional

__all__ = ["AssignedResources"]

SCHEMA = "https://schema.skao.int/ska-low-mccs-assignedresources/1.0"


class AssignedResources:
    """
    AssignedResources is the object representation of the JSON returned by the
    MCCSSubarray.assigned_resources attribute.
    """

    def __init__(
            self,
            *,  # force kwonly args
            interface: Optional[str] = SCHEMA,
            subarray_beam_ids: List[int] = None,
            station_ids: List[List[int]] = None,
            channel_blocks: List[int] = None,
    ):
        """
        Create a new object for an MCCSSubarray.assigned_resources response.

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
        self.subarray_beam_ids = list(subarray_beam_ids)
        self.station_ids = list(station_ids)
        self.channel_blocks = list(channel_blocks)

    def __eq__(self, other):
        """
        Check for equality between two AssignedResources objects.

        :param other: the object to compare to this object
        :return: returns True if the objects are equal, else False
        """
        if not isinstance(other, AssignedResources):
            return False
        return (
                self.interface == other.interface
                and self.subarray_beam_ids == other.subarray_beam_ids
                and self.station_ids == other.station_ids
                and self.channel_blocks == other.channel_blocks
        )

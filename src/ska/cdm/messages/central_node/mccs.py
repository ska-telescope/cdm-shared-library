# -*- coding: utf-8 -*-
#
# This file is part of the CDM library
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

from typing import Sequence

__all__ = ["MCCSAllocate"]


class MCCSAllocate:
    """
    MCCSAllocate is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest.
    """

    def __init__(
        self,
        station_ids: Sequence[Sequence[int]],
        channel_blocks: Sequence[int],
        subarray_beam_ids: Sequence[int],
    ):
        """
        Create a new Subarray object.

        :param station_ids: stations IDs to allocate
        :param channel_blocks: number of channel groups to assign
        :param subarray_beam_ids: station beam id's to allocate
        """
        # keep sequences as lists internally
        self.station_ids = [[int(o) for o in s] for s in station_ids]
        self.channel_blocks = [int(o) for o in channel_blocks]
        self.subarray_beam_ids = [int(o) for o in subarray_beam_ids]

    def __eq__(self, other):
        """
        Check for equality between two allocate objects

        :param other: the object to check against this allocate object
        :type other: allocate object

        :return: returns True if the objects are the same, else False
        :rtype: boolean
        """
        if not isinstance(other, MCCSAllocate):
            return False
        return (
            self.station_ids == other.station_ids
            and self.channel_blocks == other.channel_blocks
            and self.subarray_beam_ids == other.subarray_beam_ids
        )

# -*- coding: utf-8 -*-
#
# This file is part of the CDM library
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

from typing import List, Tuple

__all__ = ["MCCSAllocate"]


class MCCSAllocate:
    """
    MCCSAllocate is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest.
    """

    def __init__(
        self,
        station_ids: List[Tuple],
        channel_blocks: List[int],
        station_beam_ids: List[int],
    ):
        """
        Create a new Subarray object.

        :param station_ids: stations id's to allocate
        :type station_ids: List[Tuple]
        :param channel_blocks: number of channel groups to assign
        :type channel_blocks: List[int]
        :param station_beam_ids: station beam id's to allocate
        :type station_beam_ids: List[int]
        """
        self.station_ids = station_ids
        self.channel_blocks = list(channel_blocks)
        self.station_beam_ids = list(station_beam_ids)

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
            and self.station_beam_ids == other.station_beam_ids
        )

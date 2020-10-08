# -*- coding: utf-8 -*-
#
# This file is part of the CDM library
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

from typing import List

__all__ = ["MCCSAllocate"]


class MCCSAllocate:
    """
    MCCSAllocate is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest.
    """

    def __init__(
        self, subarray_id: int, station_ids: List[int], station_beam_ids: List[int],
    ):
        """
        Create a new Subarray object.

        :param subarray_id: the numeric SubArray ID
        :type subarray_id: int
        :param station_ids: stations id's to allocate
        :type station_ids: List[int]
        :param station_beam_ids: station beam id's to allocate
        :type station_beam_ids: List[int]
        """
        self.subarray_id = subarray_id
        self.station_ids = list(station_ids)
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
            self.subarray_id == other.subarray_id
            and self.station_ids == other.station_ids
            and self.station_beam_ids == other.station_beam_ids
        )

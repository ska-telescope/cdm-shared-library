# -*- coding: utf-8 -*-
#
# This file is part of the CDM library
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.
from ska_tmc_cdm.messages.base import CdmObject

__all__ = ["MCCSAllocate"]


class MCCSAllocate(CdmObject):
    """
    MCCSAllocate is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest.

    :param station_ids: stations IDs to allocate
    :param channel_blocks: number of channel groups to assign
    :param subarray_beam_ids: station beam id's to allocate
    """

    station_ids: list[list[int]]
    channel_blocks: list[int]
    subarray_beam_ids: list[int]

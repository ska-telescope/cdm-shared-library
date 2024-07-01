# -*- coding: utf-8 -*-
#
# This file is part of the CDM library
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

from typing import Optional

from ska_tmc_cdm.messages.base import CdmObject

__all__ = [
    "MCCSAllocate",
    "ApertureConfiguration",
    "SubArrayBeamsConfiguration",
]


class ApertureConfiguration(CdmObject):
    """
    ApertureConfiguration is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest.

    :param station_id: station id to allocate
    :param aperture_id: aperture id to allocate
    """

    station_id: Optional[int]
    aperture_id: Optional[str]


class SubArrayBeamsConfiguration(CdmObject):
    """
    SubArrayBeamsConfiguration is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest.

    :param subarray_beam_ids: beam id's to allocate
    :param apertures: list of ApertureConfiguration objects
    :param number_of_channels: number of channels to allocate
    """

    subarray_beam_id: Optional[int]
    apertures: Optional[list[ApertureConfiguration]]
    number_of_channels: Optional[int]


class MCCSAllocate(CdmObject):
    """
    MCCSAllocate is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest.

    :param station_ids: stations IDs to allocate
    :param channel_blocks: number of channel groups to assign
    :param subarray_beam_ids: station beam id's to allocate
    """

    station_ids: list[list[int]] = None
    channel_blocks: list[int] = None
    subarray_beam_ids: list[int] = None

    station_ids: list[list[int]]
    channel_blocks: list[int]
    subarray_beam_ids: list[int]

    interface: Optional[str] = None
    subarray_beams: Optional[list[SubArrayBeamsConfiguration]] = None

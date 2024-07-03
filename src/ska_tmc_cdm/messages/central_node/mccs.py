# -*- coding: utf-8 -*-
#
# This file is part of the CDM library
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

from typing import Optional

from pydantic import Field

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

    station_id: Optional[int] = None
    aperture_id: Optional[str] = None


class SubArrayBeamsConfiguration(CdmObject):
    """
    SubArrayBeamsConfiguration is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest.

    :param subarray_beam_ids: beam id's to allocate
    :param apertures: list of ApertureConfiguration objects
    :param number_of_channels: number of channels to allocate
    """

    subarray_beam_id: Optional[int] = None
    apertures: list[ApertureConfiguration] = Field(default_factory=list)
    number_of_channels: Optional[int] = None


class MCCSAllocate(CdmObject):
    """
    MCCSAllocate is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest.

    :param station_ids: stations IDs to allocate
    :param channel_blocks: number of channel groups to assign
    :param subarray_beam_ids: station beam id's to allocate
    """

    station_ids: list[list[int]] = Field(default_factory=list)
    channel_blocks: list[int] = Field(default_factory=list)
    subarray_beam_ids: list[int] = Field(default_factory=list)
    interface: Optional[str] = None
    subarray_beams: list[SubArrayBeamsConfiguration] = Field(default_factory=list)

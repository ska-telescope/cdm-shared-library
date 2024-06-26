# -*- coding: utf-8 -*-
from pydantic import Field

from ska_tmc_cdm.messages.base import CdmObject

# This file is part of the CDM library
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.
__all__ = ["AssignedResources"]

SCHEMA = "https://schema.skao.int/ska-low-mccs-assignedresources/2.0"


class AssignedResources(CdmObject):
    """
    AssignedResources is the object representation of the JSON returned by the
    MCCSSubarray.assigned_resources attribute.

    :param subarray_beam_ids: subarray beam IDs to allocate to the subarray
    :param station_ids: IDs of stations to allocate
    :param channel_blocks: channels to allocate
    :param interface: the JSON schema this object claims to be compliant with
    """

    interface: str = SCHEMA
    subarray_beam_ids: list[int] = Field(default_factory=list)
    station_ids: list[list[int]] = Field(default_factory=list)
    channel_blocks: list[int] = Field(default_factory=list)

"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import Optional

from pydantic import Field

from ska_tmc_cdm.messages.base import CdmObject

__all__ = ["CSPConfiguration", "PSSConfiguration", "PSTConfiguration"]


class PSSConfiguration(CdmObject):
    """
    Class to get PSS Configuration
    :param pss_beam_ids: List of PSS Beam IDs
    """

    pss_beam_ids: list[int] = Field(default_factory=list)


class PSTConfiguration(CdmObject):
    """
    Class to get PST Configuration
    :param pst_beam_ids: List of PST Beam IDs
    """

    pst_beam_ids: list[int] = Field(default_factory=list)


class CSPConfiguration(CdmObject):
    """
    Class to get Low CSP Configuration
    :param pss: PSS Configuration
    :param pst: PST Configuration
    """

    pss: Optional[PSSConfiguration] = None
    pst: Optional[PSTConfiguration] = None

"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import Optional

from ska_tmc_cdm.messages.base import CdmObject

__all__ = ["CSPConfiguration", "PSSConfiguration", "PSTConfiguration"]


class PSSConfiguration(CdmObject):
    """
    Class to get PSS Configuration
    """

    pss_beam_ids: Optional[list[int]] = None


class PSTConfiguration(CdmObject):
    """
    Class to get PST Configuration
    """

    pst_beam_ids: Optional[list[int]] = None


class CSPConfiguration(CdmObject):
    """
    Class to get Low CSP Configuration
    """

    pss: Optional[PSSConfiguration] = None
    pst: Optional[PSTConfiguration] = None

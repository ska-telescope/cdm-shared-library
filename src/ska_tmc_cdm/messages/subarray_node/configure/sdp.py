"""
The configure.sdp module contains Python classes that represent the various
aspects of SDP configuration that may be specified in a SubArrayNode.configure
command.
"""
from ska_tmc_cdm.messages.base import CdmObject
from typing import Optional

__all__ = ["SDPConfiguration"]

SDP_SCHEMA = "https://schema.skao.int/ska-sdp-configure/0.4"


class SDPConfiguration(CdmObject):
    """
    Message class to hold SDP configuration aspect of a
    TMC SubArrayNode.Configure call.
    """

    interface: str = SDP_SCHEMA
    transaction_id: Optional[str] = None
    scan_type: str

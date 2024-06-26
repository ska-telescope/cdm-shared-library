"""
The configure.sdp module contains Python classes that represent the various
aspects of SDP configuration that may be specified in a SubArrayNode.configure
command.
"""
from ska_tmc_cdm.messages.base import CdmObject

__all__ = ["SDPConfiguration"]

SCHEMA = "https://schema.skao.int/ska-sdp-configure/0.3"


class SDPConfiguration(CdmObject):
    """
    Message class to hold SDP configuration aspect of a
    TMC SubArrayNode.Configure call.
    """

    interface: str = SCHEMA
    scan_type: str

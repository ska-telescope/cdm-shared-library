"""
The configure.sdp module contains Python classes that represent the various
aspects of SDP configuration that may be specified in a SubArrayNode.configure
command.
"""

__all__ = ["SDPConfiguration"]

from typing import Optional

SCHEMA = "https://schema.skao.int/ska-sdp-configure/0.3"


class SDPConfiguration:
    """
    Message class to hold SDP configuration aspect of a
    TMC SubArrayNode.Configure call.
    """

    def __init__(
        self, *, interface: Optional[str] = SCHEMA, scan_type: str  # force kwonly args
    ):
        self.interface = interface
        self.scan_type = scan_type

    def __eq__(self, other):
        if not isinstance(other, SDPConfiguration):
            return False
        return self.interface == other.interface and self.scan_type == other.scan_type

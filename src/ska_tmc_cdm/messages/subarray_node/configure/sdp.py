"""
The configure.sdp module contains Python classes that represent the various
aspects of SDP configuration that may be specified in a SubArrayNode.configure
command.
"""

__all__ = ["SDPConfiguration"]

from pydantic.dataclasses import dataclass

SCHEMA = "https://schema.skao.int/ska-sdp-configure/0.3"


@dataclass(kw_only=True)
class SDPConfiguration:
    """
    Message class to hold SDP configuration aspect of a
    TMC SubArrayNode.Configure call.
    """

    interface: str = SCHEMA
    scan_type: str

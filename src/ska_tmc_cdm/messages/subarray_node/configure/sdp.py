"""
The configure.sdp module contains Python classes that represent the various
aspects of SDP configuration that may be specified in a SubArrayNode.configure
command.
"""

__all__ = ['SDPConfiguration']


class SDPConfiguration:
    """
    Class to hold SDP configuration
    """
    def __init__(self, scan_type: str):
        self.scan_type = scan_type

    def __eq__(self, other):
        if not isinstance(other, SDPConfiguration):
            return False
        return self.scan_type == other.scan_type

"""
The scan module defines simple Python representations of the structured
request for a TMC SubArrayNode.Scan command.
"""

__all__ = ["ScanRequest"]


class ScanRequest:  # pylint: disable=too-few-public-methods
    """
    ScanRequest represents the request argument for SubArrayNode.scan call.
    """

    def __init__(self, scan_id: int):
        self.scan_id = scan_id

    def __eq__(self, other):
        if not isinstance(other, ScanRequest):
            return False
        return self.scan_id == other.scan_id

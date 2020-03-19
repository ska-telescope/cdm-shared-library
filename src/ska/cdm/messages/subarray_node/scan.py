"""
The scan module defines simple Python representations of the structured
request for a TMC SubArrayNode.Scan command.
"""
from datetime import timedelta

__all__ = ['ScanRequest']


class ScanRequest:  # pylint: disable=too-few-public-methods
    """
    ScanRequest represents the request argument for SubArrayNode.scan call.
    """

    def __init__(self, scan_duration: timedelta):
        self.scan_duration = scan_duration

    def __eq__(self, other):
        if not isinstance(other, ScanRequest):
            return False
        return self.scan_duration == other.scan_duration

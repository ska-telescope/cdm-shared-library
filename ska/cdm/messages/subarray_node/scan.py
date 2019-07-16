"""
The messages module provides simple Python representations of the structured
request and response for the TMC SubArrayNode.Scan command.
"""
from datetime import timedelta

__all__ = ['ScanRequest']


# TODO write code for scan request
class ScanRequest:
    def __init__(self, scan_duration: timedelta):
        self.scan_duration = scan_duration

    def __eq__(self, other):
        if not isinstance(other, ScanRequest):
            return False
        return self.scan_duration == other.scan_duration

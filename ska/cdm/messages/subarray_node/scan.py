"""
The messages module provides simple Python representations of the structured
request and response for the TMC SubArrayNode.Scan command.
"""
from astropy.time import Time

__all__ = ['ScanRequest']


# TODO write code for scan request
class ScanRequest:
    def __init__(self, scan_duration: Time):
        self.scan_duration = scan_duration

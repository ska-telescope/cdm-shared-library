"""
The messages module provides simple Python representations of the structured
request and response for the TMC SubArrayNode.Scan command.
"""
from typing import Optional, List
from astropy.coordinates import SkyCoord

__all__ = ['ScanRequest']


# TODO write code for scan request
class ScanRequest:
    def __init__(self, scan_duration):
        self.scan_duration = scan_duration

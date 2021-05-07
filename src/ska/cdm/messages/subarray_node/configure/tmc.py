"""
Configuration specific to TMC. scan_duration (in seconds) is the duration to be used
for all scan commands following this configuration.
"""

from datetime import timedelta

__all__ = ['TMCConfiguration']


class TMCConfiguration:
    """
    Class to hold TMC configuration
    """

    def __init__(
            self, scan_duration: timedelta,
            is_ska_mid: bool = True
    ):
        self.scan_duration = scan_duration
        self.is_ska_mid = is_ska_mid

    def __eq__(self, other):
        if not isinstance(other, TMCConfiguration):
            return False
        return self.scan_duration == other.scan_duration \
               and self.is_ska_mid == other.is_ska_mid

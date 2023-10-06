"""
Configuration specific to TMC. scan_duration (in seconds) is the duration to be used
for all scan commands following this configuration.
"""
from datetime import timedelta
from typing import Optional

from pydantic.dataclasses import dataclass

__all__ = ["TMCConfiguration"]


@dataclass
class TMCConfiguration:
    """
    Class to hold TMC configuration

    :param scan_duration: Elapsed time for the scan
    """

    scan_duration: Optional[timedelta] = None
    partial_configuration: bool = False

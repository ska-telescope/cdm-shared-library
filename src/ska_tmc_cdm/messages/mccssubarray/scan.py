"""
The scan module defines Python object representations of the structured
request for an MCCSSubarray.Scan command.
"""
from dataclasses import KW_ONLY

from pydantic.dataclasses import dataclass

__all__ = ["ScanRequest"]

SCHEMA = "https://schema.skao.int/ska-low-mccs-scan/2.0"


@dataclass
class ScanRequest:  # pylint: disable=too-few-public-methods
    """
    ScanRequest represents the request argument for MCCSSubarray.Scan call.
    """

    _: KW_ONLY
    interface: str = SCHEMA
    scan_id: int
    start_time: float

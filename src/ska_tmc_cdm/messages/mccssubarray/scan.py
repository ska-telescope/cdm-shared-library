"""
The scan module defines Python object representations of the structured
request for an MCCSSubarray.Scan command.
"""

from pydantic.dataclasses import dataclass

__all__ = ["ScanRequest"]

SCHEMA = "https://schema.skao.int/ska-low-mccs-scan/2.0"


@dataclass(kw_only=True)
class ScanRequest:
    """
    ScanRequest represents the request argument for MCCSSubarray.Scan call.
    """

    interface: str = SCHEMA
    scan_id: int
    start_time: float

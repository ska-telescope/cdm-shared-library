"""
The scan module defines Python object representations of the structured
request for an MCCSSubarray.Scan command.
"""
from typing import Optional

__all__ = ["ScanRequest"]

SCHEMA = "https://schema.skao.int/ska-low-mccs-scan/2.0"


class ScanRequest:  # pylint: disable=too-few-public-methods
    """
    ScanRequest represents the request argument for MCCSSubarray.Scan call.
    """

    def __init__(
            self,
            *,  # force kwonly args
            interface: Optional[str] = SCHEMA,
            scan_id: int,
            start_time: float
    ):
        self.interface = interface
        self.scan_id = scan_id
        self.start_time = start_time

    def __eq__(self, other):
        if not isinstance(other, ScanRequest):
            return False
        return (
                self.interface == other.interface
                and self.scan_id == other.scan_id
                and self.start_time == other.start_time
        )

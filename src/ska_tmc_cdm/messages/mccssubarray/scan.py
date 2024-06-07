"""
The scan module defines Python object representations of the structured
request for an MCCSSubarray.Scan command.
"""

from pydantic.dataclasses import dataclass

__all__ = ["ScanRequest"]

SCHEMA = "https://schema.skao.int/ska-low-mccs-scan/2.0"


from ska_tmc_cdm.messages.base import CdmObject


class ScanRequest(CdmObject):
    """
    ScanRequest represents the request argument for MCCSSubarray.Scan call.
    """

    interface: str = SCHEMA
    scan_id: int
    start_time: float

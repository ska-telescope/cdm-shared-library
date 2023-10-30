"""
The scan module defines simple Python representations of the structured
request for a TMC SubArrayNode.Scan command.
"""
from typing import Optional

from pydantic.dataclasses import dataclass

__all__ = ["ScanRequest"]

# The existence of LOW_SCHEMA is an accident dating from when we thought MID
# and LOW TMC would have different schema rather than a single unified MID+LOW
# schema. LOW_SCHEMA will eventually be phased out and replaced by MID_SCHEMA,
# which will become the single schema for SubArrayNode.Scan and probably be
# renamed SCHEMA rather than SCHEMA at that point.
LOW_SCHEMA = "https://schema.skao.int/ska-low-tmc-scan/2.0"
MID_SCHEMA = "https://schema.skao.int/ska-tmc-scan/2.1"


@dataclass(kw_only=True)
class ScanRequest:
    """
    ScanRequest represents the JSON for a SubArrayNode.scan call.

    :param interface: Interface URI. Defaults to
        https://schema.skao.int/ska-tmc-scan/2.0
    :param transaction_id: optional transaction ID
    :param subarray_id: the numeric SubArray ID
    :param scan_id: integer scan ID
    """

    interface: str = MID_SCHEMA
    transaction_id: Optional[str] = None
    subarray_id: Optional[int] = None
    scan_id: int

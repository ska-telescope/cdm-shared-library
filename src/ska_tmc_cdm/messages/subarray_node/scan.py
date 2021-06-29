"""
The scan module defines simple Python representations of the structured
request for a TMC SubArrayNode.Scan command.
"""
from typing import Optional

__all__ = [
    "ScanRequest"
]

# The existence of LOW_SCHEMA is an accident dating from when we thought MID
# and LOW TMC would have different schema rather than a single unified MID+LOW
# schema. LOW_SCHEMA will eventually be phased out and replaced by MID_SCHEMA,
# which will become the single schema for SubArrayNode.Scan and probably be
# renamed SCHEMA rather than SCHEMA at that point.
LOW_SCHEMA = "https://schema.skao.int/ska-low-tmc-scan/2.0"
MID_SCHEMA = "https://schema.skao.int/ska-tmc-scan/2.0"


class ScanRequest:  # pylint: disable=too-few-public-methods
    """
    ScanRequest represents the JSON for a SubArrayNode.scan call.
    """

    def __init__(
            self,
            *,  # force kw-only args
            interface: Optional[str] = MID_SCHEMA,
            transaction_id: Optional[str] = None,
            scan_id: int,
        ):
        """
        Create a new ScanRequest.

        :param interface: Interface URI. Defaults to
            https://schema.skao.int/ska-tmc-scan/2.0
        :param transaction_id: optional transaction ID
        :param scan_id: integer scan ID
        """
        self.transaction_id = transaction_id
        self.interface = interface
        self.scan_id = scan_id

    def __eq__(self, other):
        if not isinstance(other, ScanRequest):
            return False
        return self.interface == other.interface and \
               self.transaction_id == other.transaction_id and \
               self.scan_id == other.scan_id

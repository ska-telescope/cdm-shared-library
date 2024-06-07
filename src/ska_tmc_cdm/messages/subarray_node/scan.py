"""
The scan module defines simple Python representations of the structured
request for a TMC SubArrayNode.Scan command.
"""
from typing import Optional

from pydantic import model_validator
from pydantic.dataclasses import dataclass

__all__ = ["ScanRequest"]

# The Mid and Low schema should be identical but with the addition of
# subarray_id to Low Scan schema version 4.0, the two schemas have
# diverged. In the future these schemas should be combined into one
# non-telescope specific schema.
LOW_SCHEMA = "https://schema.skao.int/ska-low-tmc-scan/4.0"
MID_SCHEMA = "https://schema.skao.int/ska-tmc-scan/2.1"


from ska_tmc_cdm.messages.base import CdmObject


class ScanRequest(CdmObject):
    """
    ScanRequest represents the JSON for a SubArrayNode.scan call.

    :param interface: Interface URI. Defaults to
        https://schema.skao.int/ska-tmc-scan/2.1 for Mid and
        https://schema.skao.int/ska-low-tmc-scan/4.0 for Low
    :param transaction_id: optional transaction ID
    :param subarray_id: the numeric SubArray ID
    :param scan_id: integer scan ID
    """

    interface: Optional[str] = None
    transaction_id: Optional[str] = None
    subarray_id: Optional[int] = None
    scan_id: int

    @model_validator(mode="after")
    def set_default_schema(self) -> "ConfigureRequest":
        if self.interface is None:
            if self.subarray_id is None:
                self.interface = MID_SCHEMA
            else:
                self.interface = LOW_SCHEMA
        return self

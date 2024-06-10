"""
Configuration specific to TMC. scan_duration (in seconds) is the duration to be used
for all scan commands following this configuration.
"""
from datetime import timedelta
from typing import Optional
from typing_extensions import Self

from pydantic import model_validator

from ska_tmc_cdm.messages.base import CdmObject

__all__ = ["TMCConfiguration"]


class TMCConfiguration(CdmObject):
    """
    Class to hold TMC configuration

    :param scan_duration: Elapsed time for the scan
    """

    scan_duration: Optional[timedelta] = None
    partial_configuration: bool = False

    @model_validator(mode="after")
    def partial_configuration_xor_scan_duration(self) -> Self:
        if self.scan_duration is not None:
            assert self.partial_configuration is False
        if self.partial_configuration is False:
            assert self.scan_duration is not None
        return self

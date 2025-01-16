"""
Configuration specific to TMC. scan_duration (in seconds) is the duration to be used
for all scan commands following this configuration.
"""
from datetime import timedelta
from typing import Callable, Optional

from pydantic import model_serializer, model_validator
from typing_extensions import Self

from ska_tmc_cdm.messages.base import CdmObject

__all__ = ["TMCConfiguration"]


class TMCConfiguration(CdmObject):
    """
    Class to hold TMC configuration

    :param scan_duration: Elapsed time for the scan
    """

    scan_duration: Optional[timedelta] = None
    partial_configuration: bool = False

    @model_serializer(mode="wrap")
    def exclude_partial_configuration_false(self, handler: Callable) -> dict:
        # TODO: Can we remove this yet? ~2024-06-20
        # Copied verbatim from Marshmallow schema:
        #     For compatibility, if partial_configuration=False (the default value)
        #     then we omit it from the output. ~2023-10-6
        #     Revisit this choice in future?
        output = handler(self)
        if self.partial_configuration is False:
            del output["partial_configuration"]
        return output

    @model_validator(mode="after")
    def scan_duration_is_mandatory_if_full_configuration(self) -> Self:
        if self.partial_configuration is False:
            assert self.scan_duration is not None
        return self

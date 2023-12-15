"""
The configure package contains modules that define Python classes for all of
the permissible arguments for a SubArrayNode.configure() call.
"""

__all__ = ["ConfigureRequest"]

from typing import Optional

from pydantic import model_validator
from pydantic.dataclasses import dataclass

from .core import DishConfiguration, PointingConfiguration
from .csp import CSPConfiguration
from .mccs import MCCSConfiguration
from .sdp import SDPConfiguration
from .tmc import TMCConfiguration

MID_SCHEMA = "https://schema.skao.int/ska-tmc-configure/2.2"
LOW_SCHEMA = "https://schema.skao.int/ska-low-tmc-configure/3.1"


@dataclass
class ConfigureRequest:  # pylint: disable=too-few-public-methods
    """
    ConfigureRequest encapsulates the arguments required for the TMC
    SubArrayNode.Configure() command.
    """

    pointing: Optional[PointingConfiguration] = None
    dish: Optional[DishConfiguration] = None
    sdp: Optional[SDPConfiguration] = None
    csp: Optional[CSPConfiguration] = None
    mccs: Optional[MCCSConfiguration] = None
    tmc: Optional[TMCConfiguration] = None
    interface: str = None
    transaction_id: Optional[str] = None

    @model_validator(mode="after")
    def partial_configuration_validation(self) -> "ConfigureRequest":
        if self.dish and self.tmc and not self.tmc.partial_configuration:
            if not self.pointing.target.coord:
                raise ValueError(
                    "ra and dec for a Target() should be defined for non-partial configuration"
                )
        return self

    @model_validator(mode="after")
    def mccs_or_dish_validation(self) -> "ConfigureRequest":
        if self.mccs is not None and (self.dish is not None):
            raise ValueError("Can't allocate dish in the same call as mccs")
        if self.mccs is None and self.dish is None and self.interface is None:
            raise ValueError("mccs, dish or interface kwarg must be set")
        elif self.mccs is not None and (self.interface is None):
            self.interface = LOW_SCHEMA
        elif self.dish is not None and (self.interface is None):
            self.interface = MID_SCHEMA
        return self

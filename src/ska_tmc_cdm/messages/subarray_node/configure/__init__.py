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

SCHEMA = "https://schema.skao.int/ska-tmc-configure/2.2"

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
    interface: Optional[str] = SCHEMA
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
            raise ValueError(
                "Can't allocate dish in the same call as mccs"
            )
        return self

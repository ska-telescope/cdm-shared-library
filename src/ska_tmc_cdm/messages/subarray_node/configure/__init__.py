"""
The configure package contains modules that define Python classes for all of
the permissible arguments for a SubArrayNode.configure() call.
"""

__all__ = ["ConfigureRequest"]

from typing import Optional

from pydantic.dataclasses import dataclass

from .core import DishConfiguration, PointingConfiguration
from .csp import CSPConfiguration
from .mccs import MCCSConfiguration
from .sdp import SDPConfiguration
from .tmc import TMCConfiguration

SCHEMA = "https://schema.skao.int/ska-tmc-configure/2.1"


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

    def __post_init__(self):
        if self.mccs is not None and (self.dish is not None):
            raise ValueError(
                "Can't allocate dish, csp and sdp in the same call as mccs"
            )

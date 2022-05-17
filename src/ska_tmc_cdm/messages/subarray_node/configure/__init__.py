"""
The configure package contains modules that define Python classes for all of
the permissible arguments for a SubArrayNode.configure() call.
"""

__all__ = ["ConfigureRequest"]

from typing import Optional

from .core import DishConfiguration, PointingConfiguration
from .csp import CSPConfiguration
from .mccs import MCCSConfiguration
from .sdp import SDPConfiguration
from .tmc import TMCConfiguration

SCHEMA = "https://schema.skao.int/ska-tmc-configure/2.0"


class ConfigureRequest:  # pylint: disable=too-few-public-methods
    """
    ConfigureRequest encapsulates the arguments required for the TMC
    SubArrayNode.Configure() command.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pointing: PointingConfiguration = None,
        dish: DishConfiguration = None,
        sdp: SDPConfiguration = None,
        csp: CSPConfiguration = None,
        mccs: MCCSConfiguration = None,
        tmc: TMCConfiguration = None,
        interface: Optional[str] = SCHEMA,
        transaction_id: Optional[str] = None,
    ):
        self.transaction_id = transaction_id
        self.pointing = pointing
        self.dish = dish
        self.sdp = sdp
        self.csp = csp
        self.tmc = tmc
        self.interface = interface
        self.mccs = mccs
        if self.mccs is not None and (self.dish is not None):
            raise ValueError(
                "Can't allocate dish, csp and sdp in the same call as mccs"
            )

    def __eq__(self, other):
        if not isinstance(other, ConfigureRequest):
            return False
        return (
            self.pointing == other.pointing
            and self.dish == other.dish
            and self.sdp == other.sdp
            and self.csp == other.csp
            and self.tmc == other.tmc
            and self.mccs == other.mccs
            and self.interface == other.interface
            and self.transaction_id == other.transaction_id
        )

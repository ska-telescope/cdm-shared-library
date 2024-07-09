"""
The configure package contains modules that define Python classes for all of
the permissible arguments for a SubArrayNode.configure() call.
"""

__all__ = ["ConfigureRequest"]

from typing import Optional

from pydantic import model_validator
from typing_extensions import Self

from .core import DishConfiguration, PointingConfiguration, SpecialTarget
from .csp import CSPConfiguration
from .mccs import MCCSConfiguration
from .sdp import SDPConfiguration
from .tmc import TMCConfiguration

MID_SCHEMA = "https://schema.skao.int/ska-tmc-configure/2.3"
LOW_SCHEMA = "https://schema.skao.int/ska-low-tmc-configure/3.1"


from ska_tmc_cdm.messages.base import CdmObject


class ConfigureRequest(CdmObject):
    """
    ConfigureRequest encapsulates the arguments required for the TMC
    SubArrayNode.Configure() command.

    :param pointing: Pointing configuration
    :param dish: Dish configuration
    :param sdp: SDP configuration
    :param csp: CSP configuration
    :param mccs: MCCS configuration
    :param tmc: TMCS configuration
    :param interface: Interface URI. Defaults to
        https://schema.skao.int/ska-tmc-configure/2.3 for Mid and
        https://schema.skao.int/ska-low-tmc-configure/3.1 for Low
    :param transaction_id: Optional transaction ID
    """

    pointing: Optional[PointingConfiguration] = None
    dish: Optional[DishConfiguration] = None
    sdp: Optional[SDPConfiguration] = None
    csp: Optional[CSPConfiguration] = None
    mccs: Optional[MCCSConfiguration] = None
    tmc: Optional[TMCConfiguration] = None
    interface: Optional[str] = None
    transaction_id: Optional[str] = None

    @model_validator(mode="after")
    def partial_configuration_validation(self) -> Self:
        if self.dish and self.tmc and not self.tmc.partial_configuration:
            if (
                self.pointing
                and self.pointing.target
                and not isinstance(self.pointing.target, SpecialTarget)
                and self.pointing.target.coord is None
            ):
                raise ValueError(
                    "ra and dec for a Target() should be defined for non-partial or sidereal configuration"
                )
        return self

    @model_validator(mode="after")
    def mccs_or_dish_validation(self) -> Self:
        if self.mccs is not None and (self.dish is not None):
            raise ValueError("Can't allocate dish in the same call as mccs")
        if self.mccs is None and self.dish is None and self.interface is None:
            raise ValueError("mccs, dish or interface kwarg must be set")
        return self

    @model_validator(mode="after")
    def set_default_schema(self) -> Self:
        if self.interface is None:
            if self.mccs is not None:
                self.interface = LOW_SCHEMA
            else:
                self.interface = MID_SCHEMA
        return self

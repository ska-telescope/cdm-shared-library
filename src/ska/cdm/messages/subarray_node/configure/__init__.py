"""
The configure package contains modules that define Python classes for all of
the permissible arguments for a SubArrayNode.configure() call.
"""
import copy

from .core import *
from .csp import *
from .sdp import *
from .tmc import *


class ConfigureRequest:  # pylint: disable=too-few-public-methods
    """
    ConfigureRequest encapsulates the arguments required for the TMC
    SubArrayNode.Configure() command.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, pointing: PointingConfiguration = None,
                 dish: DishConfiguration = None, sdp: SDPConfiguration = None,
                 csp: CSPConfiguration = None,
                 tmc: TMCConfiguration = None):
        self.pointing = pointing
        self.dish = dish
        self.sdp = sdp
        self.csp = csp
        self.tmc = tmc

    def __eq__(self, other):
        if not isinstance(other, ConfigureRequest):
            return False
        return self.pointing == other.pointing \
               and self.dish == other.dish \
               and self.sdp == other.sdp \
               and self.csp == other.csp \
               and self.tmc == other.tmc

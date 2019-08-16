"""
The configure package contains modules that define Python classes for all of
the permissible arguments for a SubArrayNode.configure() call.
"""
import copy

from .core import *
from .csp import *
from .sdp import *


class ConfigureRequest:  # pylint: disable=too-few-public-methods
    """
    ConfigureRequest encapsulates the arguments required for the TMC
    SubArrayNode.Configure() command.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, scan_id: int, pointing: PointingConfiguration = None,
                 dish: DishConfiguration = None, sdp: SDPConfiguration = None,
                 csp: CSPConfiguration = None):
        self.scan_id = scan_id
        self.pointing = pointing
        self.dish = dish
        self.sdp = sdp
        self.csp = csp

    def __eq__(self, other):
        if not isinstance(other, ConfigureRequest):
            return False
        return self.scan_id == other.scan_id \
               and self.pointing == other.pointing \
               and self.dish == other.dish \
               and self.sdp == other.sdp \
               and self.csp == other.csp

    # Until Python 3.7 the return type has to be specified as a string
    def copy_with_scan_id(self, new_scan_id: int) -> 'ConfigureRequest':
        """
        Return a copy of this ConfigureRequest with all scan IDs updated to
        the given ID.

        :param new_scan_id: new scan ID to use
        :return: updated ConfigureRequest
        """
        updated = copy.deepcopy(self)
        updated.scan_id = new_scan_id

        # update SDP scan parameters ID too
        if updated.sdp.configure:
            for pb_config in updated.sdp.configure:
                new_scan_parameters = {new_scan_id: v
                                       for _, v in pb_config.scan_parameters.items()}
                pb_config.scan_parameters = new_scan_parameters

        if updated.sdp.configure_scan:
            new_scan_parameters = {new_scan_id: v
                                   for _, v in updated.sdp.configure_scan.scan_parameters.items()}
            updated.sdp.configure_scan.scan_parameters = new_scan_parameters

        return updated

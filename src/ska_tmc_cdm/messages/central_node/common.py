"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from ska_tmc_cdm.messages.base import CdmObject

__all__ = ["DishAllocation"]


class DishAllocation(CdmObject):
    """
    DishAllocation represents the DISH allocation part of an
    AssignResources request and response.

    :param receptor_ids: (optional) IDs of the receptors to add to this
    allocation
    """

    receptor_ids: frozenset[str] = frozenset()

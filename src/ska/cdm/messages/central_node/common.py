"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import List, Optional

__all__ = ["DishAllocation"]


class DishAllocation:
    """
    DishAllocation represents the DISH allocation part of an
    AssignResources request and response.
    """

    def __init__(self, receptor_ids: Optional[List[str]] = None):
        """
        Create a new DishAllocation for the specified receptors.

        :param receptor_ids: (optional) IDs of the receptors to add to this
            allocation
        """
        if receptor_ids is None:
            receptor_ids = []
        self.receptor_ids = list(receptor_ids)

    def __eq__(self, other):
        if not isinstance(other, DishAllocation):
            return False
        return set(self.receptor_ids) == set(other.receptor_ids)

    def __repr__(self):
        return "<DishAllocation(receptor_ids={!r})>".format(self.receptor_ids)

"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from pydantic.dataclasses import dataclass


__all__ = ["DishAllocation"]


@dataclass
class DishAllocation:
    """
    DishAllocation represents the DISH allocation part of an
    AssignResources request and response.

    :param receptor_ids: (optional) IDs of the receptors to add to this
    allocation
    """
    receptor_ids: frozenset[str] = frozenset()
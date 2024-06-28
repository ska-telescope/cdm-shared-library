"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from pydantic import AliasChoices, Field

from ska_tmc_cdm.messages.base import CdmObject

__all__ = ["DishAllocation"]


class DishAllocation(CdmObject):
    """
    DishAllocation represents the DISH allocation part of an
    AssignResources request and response.

    :param receptor_ids: (optional) IDs of the receptors to add to this
        allocation

    """

    receptor_ids: frozenset[str] = Field(
        default=frozenset(),
        validation_alias=AliasChoices(
            "receptor_ids",
            # For compatibility reasons we have to accept 'receptor_ids_allocated'
            # in the context of AssignResourcesResponse.
            "receptor_ids_allocated",
        ),
    )

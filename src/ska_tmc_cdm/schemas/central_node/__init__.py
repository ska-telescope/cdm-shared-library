"""
The schemas.central_node package contains Marshmallow schemas that convert
JSON to/from the Python classes contained in ska_tmc_cdm.messages.central_node.
"""
__all__ = [
    "AssignResourcesRequestSchema",
    "AssignResourcesResponseSchema",
    "ReleaseResourcesRequestSchema",
    "StartTelescopeRequestSchema",
    "DishAllocationSchema",
    "DishAllocationResponseSchema",
    "SDPConfigurationSchema",
    "MCCSAllocateSchema",
]

from .assign_resources import (
    AssignResourcesRequestSchema,
    AssignResourcesResponseSchema,
)
from .common import DishAllocationResponseSchema, DishAllocationSchema
from .mccs import MCCSAllocateSchema
from .release_resources import ReleaseResourcesRequestSchema
from .sdp import SDPConfigurationSchema
from .telescope_start import StartTelescopeRequestSchema

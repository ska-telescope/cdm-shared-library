"""
The schemas.central_node package contains Marshmallow schemas that convert
JSON to/from the Python classes contained in ska.cdm.messages.central_node.
"""
__all__ = [
    "AssignResourcesRequestSchema",
    "AssignResourcesResponseSchema",
    "ReleaseResourcesRequestSchema",
    "DishAllocationSchema",
    "DishAllocationResponseSchema",
    "SDPConfigurationSchema",
    "MCCSAllocateSchema",
]

from .assign_resources import (
    AssignResourcesRequestSchema,
    AssignResourcesResponseSchema,
    ReleaseResourcesRequestSchema,
)

from .common import DishAllocationSchema, DishAllocationResponseSchema
from .sdp import SDPConfigurationSchema
from .mccs import MCCSAllocateSchema

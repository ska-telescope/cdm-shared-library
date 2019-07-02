"""
The ska.cdm.messages.central_node package holds modules that translate TMC
Central Node requests and responses to and from Python.
"""
from .assign_resources import AssignResourcesRequest, AssignResourcesResponse, DishAllocation
from .release_resources import ReleaseResourcesRequest
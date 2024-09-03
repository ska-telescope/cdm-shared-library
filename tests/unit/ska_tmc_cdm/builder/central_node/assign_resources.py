import functools

from ska_tmc_cdm.messages.central_node.assign_resources import (
    AssignResourcesRequest,
    AssignResourcesResponse,
)
from tests.unit.ska_tmc_cdm.builder.central_node.common import (
    DishAllocationBuilder,
)

__all__ = ["AssignResourcesRequestBuilder"]


AssignResourcesRequestBuilder = functools.partial(
    AssignResourcesRequest,
    subarray_id=1,
    transaction_id="txn-mvp01-20200325-00001",
    dish=DishAllocationBuilder(),
)


AssignResourcesResponseBuilder = functools.partial(
    AssignResourcesResponse, dish_allocation=DishAllocationBuilder()
)

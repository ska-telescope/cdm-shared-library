import functools

from ska_tmc_cdm.messages.central_node.release_resources import (
    ReleaseResourcesRequest,
)
from tests.unit.ska_tmc_cdm.builder.central_node.common import (
    DishAllocationBuilder,
)

ReleaseResourcesRequestBuilder = functools.partial(
    ReleaseResourcesRequest,
    subarray_id=1,
    dish_allocation=DishAllocationBuilder(),
    release_all=True,
    transaction_id="txn-mvp01-20200325-00001",
)

import functools

from ska_tmc_cdm.messages.central_node.common import DishAllocation

DishAllocationBuilder = functools.partial(
    DishAllocation, receptor_ids=frozenset(["SKA001"])
)

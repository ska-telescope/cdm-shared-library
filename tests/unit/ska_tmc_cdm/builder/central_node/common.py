from ska_tmc_cdm.messages.central_node.common import DishAllocation


class DishAllocateBuilder:
    """
    DishAllocateBuilder is a test data builder for CDM DishAllocate objects.

    By default, DishAllocateBuilder will build an DishAllocate

    for Mid Observation Command
    """

    def __init__(self) -> "DishAllocateBuilder":
        self.receptor_ids = None

    def set_receptor_ids(self, receptor_ids: frozenset) -> "DishAllocateBuilder":
        self.receptor_ids = receptor_ids
        return self

    def build(self) -> DishAllocation:
        return DishAllocation(receptor_ids=self.receptor_ids)

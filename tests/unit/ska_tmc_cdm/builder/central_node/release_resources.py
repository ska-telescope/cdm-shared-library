from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.release_resources import (
    ReleaseResourcesRequest,
)


class ReleaseResourcesRequestBuilder:
    """
    ReleaseResourcesRequestBuilder is a test data builder for CDM ReleaseResourcesRequest objects.

    By default, ReleaseResourcesRequestBuilder will build an ReleaseResourcesRequest

    for TMC Observation Command

    """

    def __init__(self) -> "ReleaseResourcesRequestBuilder":
        self.interface = None
        self.transaction_id = None
        self.subarray_id = None
        self.release_all = None
        self.dish_allocation = None

    def set_interface(
        self, interface: str
    ) -> "ReleaseResourcesRequestBuilder":
        """
        Set interface version
        :param: interface: Interface version
        """
        self.interface = interface
        return self

    def set_transaction_id(
        self, transaction_id: str
    ) -> "ReleaseResourcesRequestBuilder":
        """
        Set transaction ID
        :param: transaction_id: Transaction ID
        """
        self.transaction_id = transaction_id
        return self

    def set_subarray_id(
        self, subarray_id: int
    ) -> "ReleaseResourcesRequestBuilder":
        """
        Set subarray id
        :param: subarray_id: Subarray ID
        """
        self.subarray_id = subarray_id
        return self

    def set_release_all(
        self, release_all: bool
    ) -> "ReleaseResourcesRequestBuilder":
        """
        Set release all value
        :param: release_all: Release all value to either True or false
        """
        self.release_all = release_all
        return self

    def set_dish_allocation(
        self, dish_allocation: DishAllocation
    ) -> "ReleaseResourcesRequestBuilder":
        """
        Set dish allocation
        :param: dish_allocation: Dish Allocation instance
        """
        self.dish_allocation = dish_allocation
        return self

    def build(self) -> ReleaseResourcesRequest:
        """
        Builds or creates instance of CDM Release Resource Request
        """
        return ReleaseResourcesRequest(
            interface=self.interface,
            transaction_id=self.transaction_id,
            subarray_id=self.subarray_id,
            release_all=self.release_all,
            dish_allocation=self.dish_allocation,
        )

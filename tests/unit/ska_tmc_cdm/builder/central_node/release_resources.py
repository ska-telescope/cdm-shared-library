from typing_extensions import Self

from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.release_resources import ReleaseResourcesRequest


class ReleaseResourcesRequestBuilder:
    """
    ReleaseResourcesRequestBuilder is a test data builder for CDM ReleaseResourcesRequest objects.

    By default, ReleaseResourcesRequestBuilder will build an ReleaseResourcesRequest

    for TMC Observation Command

    :param interface: url string to determine JsonSchema version, defaults to
      https://schema.skao.int/ska-tmc-releaseresources/2.1 if not set
    :param transaction_id: ID for tracking requests
    :param subarray_id: the numeric SubArray ID (1..16)
    :param release_all: True to release all sub-array resources, False to
      release just those resources specified as other arguments
    :param dish_allocation: object holding the DISH resource allocation
      to release for this request.
    """

    def __init__(self) -> Self:
        self.interface = None
        self.transaction_id = None
        self.subarray_id = None
        self.release_all = None
        self.dish_allocation = None

    def set_interface(self, interface: str) -> Self:
        self.interface = interface
        return self

    def set_transaction_id(self, transaction_id: str) -> Self:
        self.transaction_id = transaction_id
        return self

    def set_subarray_id(self, subarray_id: int) -> Self:
        self.subarray_id = subarray_id
        return self

    def set_release_all(self, release_all: bool) -> Self:
        self.release_all = release_all
        return self

    def set_dish_allocation(self, dish_allocation: DishAllocation) -> Self:
        self.dish_allocation = dish_allocation
        return self

    def build(self) -> ReleaseResourcesRequest:
        return ReleaseResourcesRequest(
            interface=self.interface,
            transaction_id=self.transaction_id,
            subarray_id=self.subarray_id,
            release_all=self.release_all,
            dish_allocation=self.dish_allocation,
        )

"""
The telescope_start module provides simple Python representations of the
structured request and response for a TMC CentralNode.start
"""
from typing import Optional

__all__ = ["StartTelescopeRequest"]


class StartTelescopeRequest:
    def __init__(
        self,
        subarray_id: Optional[int] = None,
        interface: Optional[str] = None,
        transaction_id: str = None,
    ):
        """
        Create a new StartTelescopeRequest object
        :param subarray_id: the numeric SubArray ID (1..16)
        :param interface: url string to determine JsonSchema version
        :param transaction_id: ID for tracking requests
        """
        self.subarray_id = subarray_id
        self.interface = interface
        self.transaction_id = transaction_id

    def __eq__(self, other):
        if not isinstance(other, StartTelescopeRequest):
            return False
        return (
            self.subarray_id == other.subarray_id
            and self.interface == other.interface
            and self.transaction_id == other.transaction_id
        )

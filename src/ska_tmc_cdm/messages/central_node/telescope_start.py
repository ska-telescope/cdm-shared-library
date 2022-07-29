"""
The start_telescope module provides simple Python representations of the
structured request and response for a TMC CentralNode.start
"""


class StartTelescope:
    def __init__(self, subarray_id:int=None, transaction_id:str=None):
 
        """
        Create a new StartTelescope object.

        :param transaction_id: ID for tracking requests
        :param subarray_id: the numeric SubArray ID (1..16)
        """
        self.subarray_id = subarray_id
        self.transaction_id = transaction_id
    def __eq__(self, other):
        if not isinstance(other, StartTelescope):
            return False
        return (
            self.transaction_id == other.transaction_id
            and self.subarray_id == other.subarray_id
        )
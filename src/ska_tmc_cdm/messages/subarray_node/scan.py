"""
The scan module defines simple Python representations of the structured
request for a TMC SubArrayNode.Scan command.
"""

__all__ = ["ScanRequest"]


class ScanRequest:  # pylint: disable=too-few-public-methods
    """
    ScanRequest represents the request argument for SubArrayNode.scan call.
    """

    def __init__(
            self, 
            scan_id: int, 
            interface: str = None, 
            transaction_id: str = None
        ):
        self.transaction_id = transaction_id
        self.interface = interface
        self.scan_id = scan_id

    def __eq__(self, other):
        if not isinstance(other, ScanRequest):
            return False
        return self.interface == other.interface and \
               self.scan_id == other.scan_id and \
               self.transaction_id == other.transaction_id

from ska_tmc_cdm.messages.subarray_node.scan import ScanRequest


class ScanRequestBuilder:
    """
    ScanRequestBuilder is a test data builder for CDM ScanRequest objects.

    """

    def __init__(self):
        """
        :param interface: Interface URI. Defaults to
            https://schema.skao.int/ska-tmc-scan/2.1 for Mid and
            https://schema.skao.int/ska-low-tmc-scan/4.0 for Low
        :param transaction_id: optional transaction ID
        :param subarray_id: the numeric SubArray ID
        :param scan_id: integer scan ID
        """
        self.interface = None
        self.transaction_id = None
        self.subarray_id = None
        self.scan_id = None

    def set_interface(self, interface: str) -> "ScanRequestBuilder":
        """
        Set schema interface
        :param: interface: interface version
        """
        self.interface = interface
        return self

    def set_transaction_id(self, transaction_id: str) -> "ScanRequestBuilder":
        """
        Set transaction id
        :param: transaction_id: Transaction ID
        """
        self.transaction_id = transaction_id
        return self

    def set_subarray_id(self, subarray_id: int) -> "ScanRequestBuilder":
        """
        Set Subarray ID
        :param: Subarray ID
        """
        self.subarray_id = subarray_id
        return self

    def set_scan_id(self, scan_id: int) -> "ScanRequestBuilder":
        """
        Set scan ID
        :param: scan_id: Scan ID
        """
        self.scan_id = scan_id
        return self

    def build(self) -> "ScanRequestBuilder":
        """
        Builds or creates instance of CDM Scan Request
        """
        return ScanRequest(
            interface=self.interface,
            transaction_id=self.transaction_id,
            subarray_id=self.subarray_id,
            scan_id=self.scan_id,
        )

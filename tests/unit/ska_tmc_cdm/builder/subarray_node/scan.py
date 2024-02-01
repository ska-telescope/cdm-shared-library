from ska_tmc_cdm.messages.subarray_node.scan import LOW_SCHEMA, MID_SCHEMA, ScanRequest

class ScanRequestBuilder:
    def __init__(self):
        self.interface = None
        self.transaction_id = None
        self.subarray_id = None
        self.scan_id = None
    
    def set_interface(self, interface: str) -> "ScanRequestBuilder":
        self.interface = interface
        return self

    def set_transaction_id(
            self, transaction_id: str
    ) -> "ScanRequestBuilder":
        self.transaction_id = transaction_id
        return self

    def set_subarray_id(self, subarray_id: int) -> "ScanRequestBuilder":
        self.subarray_id = subarray_id
        return self


    def set_scan_id(self, scan_id: int) -> "ScanRequestBuilder":
        self.scan_id = scan_id
        return self

    def build(self) -> "ScanRequestBuilder":
        return ScanRequest(interface=self.interface,
                           transaction_id=self.transaction_id,
                           subarray_id = self.subarray_id,
                           scan_id = self.scan_id

        )

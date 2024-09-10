import functools

from ska_tmc_cdm.messages.subarray_node.scan import MID_SCHEMA, ScanRequest

ScanRequestBuilder = functools.partial(
    ScanRequest,
    interface=MID_SCHEMA,
    transaction_id="txn-....-00001",
    scan_id=123,
    subarray_id=1,
)

"""
Unit tests for the messages>central_node>telescope_start module.
"""
from ska_tmc_cdm.messages.central_node.telescope_start import StartTelescopeRequest

NULL_TRANSACTION_ID = None
NULL_INTERFACE = None
SAMPLE_SUBARRAY_ID = 1


def test_start_telescope_eq():
    """
    Verify that two StartTelescopeRequest with the same subarray_id are
    considered equal else unequal.
    """
    start_telescope = StartTelescopeRequest(1)
    assert start_telescope == StartTelescopeRequest(
        SAMPLE_SUBARRAY_ID, NULL_INTERFACE, NULL_TRANSACTION_ID
    )
    # ... different transaction id, subarray id ...
    assert start_telescope != StartTelescopeRequest(
        3, "https://schema.skao.int/ska-sdp-telestart/1.0", "txn-ts01-20220803-00004"
    )


def test_start_telescope_eq_with_other_objects():
    """
    Verify that a StartTelescopeRequest is considered unequal to objects of other
    types.
    """
    start_telescope = StartTelescopeRequest()
    assert start_telescope != object()

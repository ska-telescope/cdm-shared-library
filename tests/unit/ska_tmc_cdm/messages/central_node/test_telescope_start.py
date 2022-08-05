"""
Unit tests for the messages>central_node>telescope_start module.
"""
from ska_tmc_cdm.messages.central_node.telescope_start import StartTelescope

NULL_TRANSACTION_ID = None
SAMPLE_SUBARRAY_ID = 1


def test_start_telescope_eq():
    """
    Verify that two StartTelescope with the same subarray_id are
    considered equal else unequal.
    """
    start_telescope = StartTelescope(1)
    assert start_telescope == StartTelescope(SAMPLE_SUBARRAY_ID, NULL_TRANSACTION_ID)
    # ... different transaction id, subarray id ...
    assert start_telescope != StartTelescope("sample_transaction_id", 3)


def test_start_telescope_eq_with_other_objects():
    """
    Verify that a StartTelescope is considered unequal to objects of other
    types.
    """
    start_telescope = StartTelescope()
    assert start_telescope != object()

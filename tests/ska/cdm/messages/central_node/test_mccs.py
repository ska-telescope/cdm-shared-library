"""
Unit tests for the CentralNode.mccs allocate module.
"""


from ska.cdm.messages.central_node.mccs import MCCSAllocate


def test_mccs_allocate_eq():
    """
    Verify that two MCCSAllocate objects with the same allocated elements are
    considered equal.
    """
    mccs_allocate = MCCSAllocate(
        1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate == MCCSAllocate(
        1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate != MCCSAllocate(
        2, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate != MCCSAllocate(
        1, [2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate != MCCSAllocate(
        1, [1, 2, 3, 4], [3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate != MCCSAllocate(
        1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7]
    )


def test_mccs_allocate_eq_with_other_objects():
    """
    Verify that a MCCSAllocate is considered unequal to objects of other
    types.
    """
    mccs_allocate = MCCSAllocate(
        1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    assert mccs_allocate != 1
    assert mccs_allocate != object()

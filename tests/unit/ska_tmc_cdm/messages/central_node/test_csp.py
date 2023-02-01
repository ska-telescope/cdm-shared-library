"""
Unit tests for the CentralNode.AssignResources csp module.
"""
from ska_tmc_cdm.messages.central_node.csp import (
    CommonConfiguration,
    CSPConfiguration,
    LowCbfConfiguration,
    ResourcesConfiguration,
)

# example valid interface
valid_iface = "https://schema.skao.int/ska-low-csp-assignresources/2.0"
# example valid lowcbf
valid_lowcbf = LowCbfConfiguration(
    resources=[
        ResourcesConfiguration(
            device="fsp_01", shared=True, fw_image="pst", fw_mode="unused"
        ),
        ResourcesConfiguration(
            device="p4_01", shared=True, fw_image="p4.bin", fw_mode="p4"
        ),
    ]
)
# example valid common
valid_comm = CommonConfiguration(subarray_id=1)
# valid CSP with these inputs
valid_obj = CSPConfiguration(
    interface=valid_iface, lowcbf=valid_lowcbf, common=valid_comm
)


def test_valid():
    """
    Verify that CSP object is created when valid input
    """

    assert valid_obj.interface == valid_iface
    assert valid_obj.common == valid_comm
    assert valid_obj.lowcbf == valid_lowcbf


def test_eq():
    """
    Verify that two different CSP objects of same values considered equal
    """
    test_obj = CSPConfiguration(
        interface=valid_iface, lowcbf=valid_lowcbf, common=valid_comm
    )
    assert test_obj == valid_obj
    # however should be unequal for different value of interface
    assert valid_obj != CSPConfiguration(
        interface="2.0", lowcbf=valid_lowcbf, common=valid_comm
    )
    # however should be unequal from any other object
    test_obj = CSPConfiguration(
        interface=valid_iface, lowcbf=valid_lowcbf, common=valid_comm
    )
    assert test_obj != int(1)
    assert test_obj != object

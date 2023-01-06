"""
Unit tests for the CentralNode.AssignResources csp module.
"""
import copy

import pytest

from ska_tmc_cdm.messages.central_node.csp import CSPConfiguration

# example valid interface
valid_iface = "https://schema.skao.int/ska-low-csp-assignresources/2.0"
# example valid lowcbf
valid_lowcbf = {
    "resources": [
        {"device": "p4_01", "shared": True, "fw_image": "pst", "fw_mode": "unused"},
        {"device": "pst", "shared": False, "fw_image": "p4.bin", "fw_mode": "p4"},
    ]
}
# example valid common
valid_comm = {"subarray_id": 1}
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


def test_err():
    """
    Verify that key for missing mandatory key and type errors for mismatch in data type are raised
    """
    # resources missing
    lowcbf_missing_key1 = {
        "device": "p4_01",
        "shared": True,
        "fw_image": "pst",
        "fw_mode": "unused",
    }
    # fw_image key missing
    lowcbf_missing_key2 = valid_lowcbf
    del dict(lowcbf_missing_key2["resources"][1])["fw_image"]
    # checking KeyError raised
    with pytest.raises(KeyError):
        CSPConfiguration(
            interface=valid_iface, lowcbf=lowcbf_missing_key1, common=valid_comm
        )
        CSPConfiguration(
            interface=valid_iface, lowcbf=lowcbf_missing_key2, common=valid_comm
        )
    # checking TypeError raised
    # interface not given str value
    with pytest.raises(TypeError):
        CSPConfiguration(interface=2.0, lowcbf=valid_lowcbf, common=valid_comm)
    # 'subarray_id' not given a int
    with pytest.raises(TypeError):
        CSPConfiguration(
            interface=valid_iface, lowcbf=valid_lowcbf, common={"subarray_id": "1"}
        )

    # device given int instead of str
    lowcbf_device_int = copy.deepcopy(valid_lowcbf)
    lowcbf_device_int["resources"][0]["device"] = 0
    with pytest.raises(TypeError):
        CSPConfiguration(
            interface=valid_iface, lowcbf=lowcbf_device_int, common=valid_comm
        )
    # shared given int instead of bool
    lowcbf_shared_int = copy.deepcopy(valid_lowcbf)
    lowcbf_shared_int["resources"][0]["shared"] = 20
    with pytest.raises(TypeError):
        CSPConfiguration(
            interface=valid_iface, lowcbf=lowcbf_shared_int, common=valid_comm
        )
    # fw_image given int instead of str
    lowcbf_image_int = copy.deepcopy(valid_lowcbf)
    lowcbf_image_int["resources"][0]["fw_image"] = 8
    with pytest.raises(TypeError):
        CSPConfiguration(
            interface=valid_iface, lowcbf=lowcbf_image_int, common=valid_comm
        )
    # fw_mode given int instead of str
    lowcbf_mode_int = copy.deepcopy(valid_lowcbf)
    lowcbf_mode_int["resources"][0]["fw_mode"] = 9
    with pytest.raises(TypeError):
        CSPConfiguration(
            interface=valid_iface, lowcbf=lowcbf_mode_int, common=valid_comm
        )

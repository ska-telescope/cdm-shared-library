"""
Unit tests for the CentralNode.AssignResources csp module.
"""


from tests.unit.ska_tmc_cdm.builder.central_node.csp import (
    CommonConfigurationBuilder,
    CSPConfigurationBuilder,
    LowCbfConfigurationBuilder,
    ResourceConfigurationBuilder,
)


def common_config(subarray_id=None):
    common1 = (
        CommonConfigurationBuilder().set_subarray_id(subarray_id=subarray_id).build()
    )
    return common1


def resources_conf(device=None, shared=None, fw_image=None, fw_mode=None):
    resource = (
        ResourceConfigurationBuilder()
        .set_device(device=device)
        .set_shared(shared=shared)
        .set_fw_image(fw_image=fw_image)
        .set_fw_mode(fw_mode=fw_mode)
        .build()
    )
    return resource


def lowcbf_conf(resources=None):
    lowcbf1 = LowCbfConfigurationBuilder().set_resources(resources=resources)
    return lowcbf1


def csp_config(interface=None, common=None, lowcbf=None):
    csp1 = (
        CSPConfigurationBuilder()
        .set_interface(interface=interface)
        .set_common(common=common)
        .set_lowcbf(lowcbf=lowcbf)
        .build()
    )
    return csp1


interface1 = "https://schema.skao.int/ska-low-csp-assignresources/2.0"
resource1 = resources_conf(
    device="fsp_01", shared=True, fw_image="pst", fw_mode="unused"
)
resource2 = resources_conf(device="p4_01", shared=True, fw_image="p4.bin", fw_mode="p4")
lowcbf2 = lowcbf_conf(resources=[resource1, resource2])
common2 = common_config(subarray_id=1)

valid_obj = csp_config(interface=interface1, common=common2, lowcbf=lowcbf2)


def test_valid():
    """
    Verify that CSP object is create valid_command when valid input
    """
    assert valid_obj.interface == interface1
    assert valid_obj.common == common2
    assert valid_obj.lowcbf == lowcbf2


def test_eq():
    """
    Verify that two different CSP objects of same values considered equal
    """
    valid_obj2 = csp_config(interface=interface1, common=common2, lowcbf=lowcbf2)
    assert valid_obj == valid_obj2
    assert valid_obj != int(1)
    assert valid_obj != object

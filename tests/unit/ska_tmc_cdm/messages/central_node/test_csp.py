"""
Unit tests for the CentralNode.AssignResources csp module.
"""


from tests.unit.ska_tmc_cdm.builder_pattern.central_node.csp import (
    CommonConfigurationBuilder,
    CSPConfigurationBuilder,
    LowCbfConfigurationBuilder,
    ResourceConfigurationBuilder,
)


def common_config(subarray_id):
    common = (
        CommonConfigurationBuilder().set_subarray_id(subarray_id=subarray_id).build()
    )
    return common


def resources(device, shared, fw_image, fw_mode):
    resource = (
        ResourceConfigurationBuilder()
        .set_device(device=device)
        .set_shared(shared=shared)
        .set_fw_image(fw_image=fw_image)
        .set_fw_mode(fw_mode=fw_mode)
        .build()
    )
    return resource


def lowcbf(resources):
    lowcbf = LowCbfConfigurationBuilder().set_resources(resources=resources)
    return lowcbf


def csp_config(interface, common, lowcbf):
    csp = (
        CSPConfigurationBuilder()
        .set_interface(interface=interface)
        .set_common(common=common)
        .set_lowcbf(lowcbf=lowcbf)
        .build()
    )
    return csp


interface = "https://schema.skao.int/ska-low-csp-assignresources/2.0"
resource1 = resources(device="fsp_01", shared=True, fw_image="pst", fw_mode="unused")
resource2 = resources(device="p4_01", shared=True, fw_image="p4.bin", fw_mode="p4")
lowcbf = lowcbf(resources=[resource1, resource2])
common = common_config(subarray_id=1)

valid_obj = csp_config(interface=interface, common=common, lowcbf=lowcbf)


def test_valid():
    """
    Verify that CSP object is create valid_command when valid input
    """
    assert valid_obj.interface == interface
    assert valid_obj.common == common
    assert valid_obj.lowcbf == lowcbf


def test_eq():
    """
    Verify that two different CSP objects of same values considered equal
    """
    valid_obj2 = csp_config(interface=interface, common=common, lowcbf=lowcbf)
    assert valid_obj == valid_obj2
    assert valid_obj != int(1)
    assert valid_obj != object

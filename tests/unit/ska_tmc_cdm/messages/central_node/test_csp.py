"""
Unit tests for the CentralNode.AssignResources csp module.
"""

from tests.unit.ska_tmc_cdm.builder.central_node.csp import (
    CommonConfigurationBuilder,
    CSPConfigurationBuilder,
    LowCbfConfigurationBuilder,
    ResourceConfigurationBuilder,
)


def csp_configuration_builder(interface=None, common=None, lowcbf=None):
    """This csp configuration builder is a test data builder for CDM csp configuration"""
    return (
        CSPConfigurationBuilder()
        .set_interface(interface=interface)
        .set_common(common=common)
        .set_lowcbf(lowcbf=lowcbf)
        .build()
    )


def common_configuration_builder(subarray_id=None):
    """This common configuration builder is a test data builder for CDM common configuration"""
    return CommonConfigurationBuilder().set_subarray_id(subarray_id=subarray_id).build()


def lowcbf_configuration_builder(resources=None):
    """This lowcbf configuration builder is a test data builder for CDM lowcbf configuration"""
    return LowCbfConfigurationBuilder().set_resources(resources=resources).build()


def resource_configuration_builder(
    device=None, shared=None, fw_image=None, fw_mode=None
):
    """This resource configuration builder is a test data builder for CDM resource configuration"""
    return (
        ResourceConfigurationBuilder()
        .set_device(device=device)
        .set_shared(shared=shared)
        .set_fw_image(fw_image=fw_image)
        .set_fw_mode(fw_mode=fw_mode)
        .build()
    )


interface1 = "https://schema.skao.int/ska-low-csp-assignresources/2.0"
resource1 = resource_configuration_builder(
    device="fsp_01", shared=True, fw_image="pst", fw_mode="unused"
)
resource2 = resource_configuration_builder(
    device="p4_01", shared=True, fw_image="p4.bin", fw_mode="p4"
)
lowcbf2 = lowcbf_configuration_builder(resources=[resource1, resource2])
common2 = common_configuration_builder(subarray_id=1)

valid_obj = csp_configuration_builder(
    interface=interface1, common=common2, lowcbf=lowcbf2
)


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
    valid_obj2 = csp_configuration_builder(
        interface=interface1, common=common2, lowcbf=lowcbf2
    )
    assert valid_obj == valid_obj2
    assert valid_obj != int(1)
    assert valid_obj != object

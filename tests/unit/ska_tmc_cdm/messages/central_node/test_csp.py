"""
Unit tests for the CentralNode.AssignResources csp module.
"""


from tests.unit.ska_tmc_cdm.builder_pattern.central_node.csp import CSPConfigurationBuilder, CommonConfigurationBuilder, LowCbfConfigurationBuilder, ResourceConfigurationBuilder


interface = "https://schema.skao.int/ska-low-csp-assignresources/2.0"
lowcbf = (
    LowCbfConfigurationBuilder()
    .setresources(
        resources=[
            ResourceConfigurationBuilder()
            .setdevice(device="fsp_01")
            .setshared(shared=True)
            .setfw_image(fw_image="pst")
            .setfw_mode(fw_mode="unused")
            .build(),
            ResourceConfigurationBuilder()
            .setdevice(device="p4_01")
            .setshared(shared=True)
            .setfw_image(fw_image="p4.bin")
            .setfw_mode(fw_mode="p4")
            .build(),
        ]
    )
    .build()
)
common = CommonConfigurationBuilder().setsubarray_id(subarray_id=1).build()
valid_obj = (
    CSPConfigurationBuilder()
    .setinterface(interface=interface)
    .setcommon(common=common)
    .setlowcbf(lowcbf=lowcbf)
    .build()
)


def test_valid():
    """
    Verify that CSP object is crevalid_commated when valid input
    """
    assert valid_obj.interface == interface
    assert valid_obj.common == common
    assert valid_obj.lowcbf == lowcbf


def test_eq():
    """
    Verify that two different CSP objects of same values considered equal
    """
    valid_obj2 = (
        CSPConfigurationBuilder()
        .setinterface(interface=interface)
        .setcommon(common=common)
        .setlowcbf(lowcbf=lowcbf)
        .build()
    )
    assert valid_obj == valid_obj2
    assert valid_obj != int(1)
    assert valid_obj != object

"""
Unit tests for the CentralNode.AssignResources csp module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.central_node.csp import (
    CommonConfigurationBuilder,
    CSPConfigurationBuilder,
    LowCbfConfigurationBuilder,
    ResourceConfigurationBuilder,
)

interface = "https://schema.skao.int/ska-low-csp-assignresources/2.0"


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            CSPConfigurationBuilder()
            .set_interface(interface)
            .set_common(
                CommonConfigurationBuilder().set_subarray_id(subarray_id=1).build()
            )
            .set_lowcbf(
                LowCbfConfigurationBuilder()
                .set_resources(
                    [
                        ResourceConfigurationBuilder()
                        .set_device("fsp_01")
                        .set_shared(True)
                        .set_fw_image("pst")
                        .set_fw_mode("unused")
                        .build()
                    ]
                )
                .build()
            )
            .build(),
            CSPConfigurationBuilder()
            .set_interface(interface)
            .set_common(
                CommonConfigurationBuilder().set_subarray_id(subarray_id=1).build()
            )
            .set_lowcbf(
                LowCbfConfigurationBuilder()
                .set_resources(
                    [
                        ResourceConfigurationBuilder()
                        .set_device("fsp_01")
                        .set_shared(True)
                        .set_fw_image("pst")
                        .set_fw_mode("unused")
                        .build()
                    ]
                )
                .build()
            )
            .build(),
            True,
        ),
        (  # not equal
            CSPConfigurationBuilder()
            .set_interface(interface)
            .set_common(
                CommonConfigurationBuilder().set_subarray_id(subarray_id=1).build()
            )
            .set_lowcbf(
                LowCbfConfigurationBuilder()
                .set_resources(
                    [
                        ResourceConfigurationBuilder()
                        .set_device("fsp_01")
                        .set_shared(True)
                        .set_fw_image("pst")
                        .set_fw_mode("unused")
                        .build()
                    ]
                )
                .build()
            )
            .build(),
            CSPConfigurationBuilder()
            .set_interface(interface)
            .set_common(
                CommonConfigurationBuilder().set_subarray_id(subarray_id=1).build()
            )
            .set_lowcbf(
                LowCbfConfigurationBuilder()
                .set_resources(
                    [
                        ResourceConfigurationBuilder()
                        .set_device("p4_01")
                        .set_shared(True)
                        .set_fw_image("pst")
                        .set_fw_mode("unused")
                        .build()
                    ]
                )
                .build()
            )
            .build(),
            False,
        ),
    ],
)
def test_csp_eq_check(object1, object2, is_equal):
    """
    Verify  object  of CSP with same properties are equal
    And with different properties are different and also check equality with different object
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()

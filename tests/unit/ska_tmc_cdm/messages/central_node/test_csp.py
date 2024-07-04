"""
Unit tests for the CentralNode.AssignResources csp module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.central_node.csp import (
    CSPConfigurationBuilder,
    PSSConfigurationBuilder,
    PSTConfigurationBuilder,
)


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            CSPConfigurationBuilder()
            .set_pss(
                PSSConfigurationBuilder().set_pss_beam_ids([1, 2, 3]).build()
            )
            .set_pst(PSTConfigurationBuilder().set_pst_beam_ids([1]).build())
            .build(),
            CSPConfigurationBuilder()
            .set_pss(
                PSSConfigurationBuilder().set_pss_beam_ids([1, 2, 3]).build()
            )
            .set_pst(PSTConfigurationBuilder().set_pst_beam_ids([1]).build())
            .build(),
            True,
        ),
        (  # not equal
            CSPConfigurationBuilder()
            .set_pss(
                PSSConfigurationBuilder().set_pss_beam_ids([1, 2, 3]).build()
            )
            .set_pst(PSTConfigurationBuilder().set_pst_beam_ids([1]).build())
            .build(),
            CSPConfigurationBuilder()
            .set_pss(
                PSSConfigurationBuilder().set_pss_beam_ids([1, 2, 3]).build()
            )
            .set_pst(PSTConfigurationBuilder().set_pst_beam_ids([2]).build())
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

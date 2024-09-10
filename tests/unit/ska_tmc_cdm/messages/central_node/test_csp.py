"""
Unit tests for the CentralNode.AssignResources csp module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.central_node.csp import (
    CSPConfigurationBuilder,
    PSSConfigurationBuilder,
)


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            CSPConfigurationBuilder(),
            CSPConfigurationBuilder(),
            True,
        ),
        (  # not equal
            CSPConfigurationBuilder(pss=PSSConfigurationBuilder()),
            CSPConfigurationBuilder(pss=None),
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

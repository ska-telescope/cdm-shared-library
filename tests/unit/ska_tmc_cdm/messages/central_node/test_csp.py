"""
Unit tests for the CentralNode.AssignResources csp module.
"""


from polyfactory.factories import DataclassFactory

from ska_tmc_cdm.messages.central_node.csp import (
    CommonConfiguration,
    CSPConfiguration,
    LowCbfConfiguration,
    ResourceConfiguration,
)


class CommonConfigurationFactory(DataclassFactory[CommonConfiguration]):
    __model__ = CommonConfiguration


class CSPConfigurationFactory(DataclassFactory[CSPConfiguration]):
    __model__ = CSPConfiguration


class LowCbfConfigurationFactory(DataclassFactory[LowCbfConfiguration]):
    __model__ = LowCbfConfiguration


class ResourceConfigurationConfigurationFactory(
    DataclassFactory[ResourceConfiguration]
):
    __model__ = ResourceConfiguration


interface1 = "https://schema.skao.int/ska-low-csp-assignresources/2.0"

resource1 = ResourceConfigurationConfigurationFactory.build()
resource2 = ResourceConfigurationConfigurationFactory.build()
lowcbf2 = LowCbfConfigurationFactory.build(resources=[resource1, resource2])
common2 = CommonConfigurationFactory.build(subarray_id=1)

valid_obj = CSPConfigurationFactory.build(
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
    valid_obj2 = CSPConfigurationFactory.build(
        interface=interface1, common=common2, lowcbf=lowcbf2
    )
    assert valid_obj == valid_obj2
    assert valid_obj != int(1)
    assert valid_obj != object

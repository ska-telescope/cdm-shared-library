"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.pst module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.pst import (
    PSTBeamConfigurationBuilder,
    PSTConfigurationBuilder,
    PSTScanConfigurationBuilder,
)


@pytest.mark.parametrize(
    "pst_configuration_1, pst_configuration_2, is_equal",
    [
        (
            PSTConfigurationBuilder(),
            PSTConfigurationBuilder(),
            True,
        ),
        (
            PSTConfigurationBuilder(
                beams=[
                    PSTBeamConfigurationBuilder(
                        scan=PSTScanConfigurationBuilder(
                            receptors=["receptor1", "receptor2"]
                        )
                    )
                ]
            ),
            PSTConfigurationBuilder(
                beams=[
                    PSTBeamConfigurationBuilder(
                        scan=PSTScanConfigurationBuilder(
                            receptors=["receptor2", "receptor3"]
                        )
                    )
                ]
            ),
            False,
        ),
    ],
)
def test_pst_configuration_builder(
    pst_configuration_1, pst_configuration_2, is_equal
):
    """
    Test the PSTConfigurationBuilder class.

    :param pst_configuration_1: The first PSTConfiguration object to compare.
    :type pst_configuration_1: PSTConfiguration
    :param pst_configuration_2: The second PSTConfiguration object to compare.
    :type pst_configuration_2: PSTConfiguration
    :param is_equal: Whether the two objects are equal or not.
    :type is_equal: bool
    """
    assert (pst_configuration_1 == pst_configuration_2) == is_equal
    assert pst_configuration_1 != 1
    assert pst_configuration_1 != object

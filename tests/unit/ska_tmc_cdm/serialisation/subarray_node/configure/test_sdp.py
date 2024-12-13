"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure.sdp module.
"""

import pytest

from ska_tmc_cdm.messages.subarray_node.configure import SDPConfiguration
from tests.unit.ska_tmc_cdm.serialisation import serialisation_utils as utils

VALID_JSON = """
{
    "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
    "scan_type": "science_A"
}
"""

VALID_OBJECT = SDPConfiguration(scan_type="science_A")


@pytest.mark.parametrize(
    "model_class,instance,modifier_fn,valid_json,invalid_json",
    [
        (SDPConfiguration, VALID_OBJECT, None, VALID_JSON, None),
    ],
)
def test_releaseresources_serialisation_and_validation(
    model_class, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_serialisation_and_validation(
        model_class, instance, modifier_fn, valid_json, invalid_json
    )

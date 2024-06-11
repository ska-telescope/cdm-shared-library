"""
Unit tests for serialisation of ska_tmc_cdm modules.
"""

import pytest

from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate

from .. import utils

VALID_MCCSALLOCATE_JSON = """
{
    "station_ids": [[1, 2]],
    "channel_blocks": [1, 2, 3, 4, 5],
    "subarray_beam_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9]
}
"""

VALID_MCCSALLOCATE_OBJECT = MCCSAllocate(
    station_ids=[(1, 2)],
    channel_blocks=[1, 2, 3, 4, 5],
    subarray_beam_ids=[1, 2, 3, 4, 5, 6, 7, 8, 9],
)


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            MCCSAllocate,
            VALID_MCCSALLOCATE_OBJECT,
            None,  # no validation on subschema
            VALID_MCCSALLOCATE_JSON,
            None,
        ),  # no validation on subschema
    ],
)
def test_releaseresources_serialisation_and_validation(
    cdm_class, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that the model marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        cdm_class, instance, modifier_fn, valid_json, invalid_json
    )

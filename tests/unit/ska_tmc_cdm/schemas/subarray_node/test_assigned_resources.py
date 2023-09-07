from pathlib import Path

import pytest
from vcr import VCR

from ska_tmc_cdm.messages.subarray_node.assigned_resources import (
    AssignedResources,
    MCCSAllocation,
)
from ska_tmc_cdm.schemas.subarray_node.assigned_resources import (
    AssignedResourcesSchema,
    MCCSAllocationSchema,
)

from .. import utils

HERE = Path(__file__).parent.resolve()

vcrpy = VCR(
    cassette_library_dir=str(HERE / "canned_http_responses"),
    path_transformer=VCR.ensure_suffix(".yaml"),
)

VALID_MCCSALLOCATION_JSON = """
{
    "subarray_beam_ids": [1],
    "station_ids": [ [1,2] ],
    "channel_blocks": [3]
}
"""

VALID_MCCSALLOCATION_OBJECT = MCCSAllocation(
    subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
)

VALID_ASSIGNEDRESOURCES_JSON = (
    """
{
  "interface": "https://schema.skao.int/ska-low-tmc-assignedresources/2.0",
  "mccs": """
    + VALID_MCCSALLOCATION_JSON
    + """
}
"""
)

VALID_ASSIGNEDRESOURCES_OBJECT = AssignedResources(
    interface="https://schema.skao.int/ska-low-tmc-assignedresources/2.0",
    mccs=VALID_MCCSALLOCATION_OBJECT,
)

INVALID_ASSIGNEDRESOURCES_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-tmc-assignedresources/2.0",
  "mccs": {
    "subarray_beam_ids": [-1],
    "station_ids": [ [1,2] ],
    "channel_blocks": [3]
  }
}
"""


def invalidate_assignresources(o: AssignedResources):
    # function to make a valid AssignedResources invalid
    o.mccs.subarray_beam_ids = [-1]


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            AssignedResourcesSchema,
            VALID_ASSIGNEDRESOURCES_OBJECT,
            invalidate_assignresources,
            VALID_ASSIGNEDRESOURCES_JSON,
            INVALID_ASSIGNEDRESOURCES_JSON,
        ),
        (
            MCCSAllocationSchema,
            VALID_MCCSALLOCATION_OBJECT,
            None,  # no validation on MCCSAllocation subschema
            VALID_MCCSALLOCATION_JSON,
            None,
        ),  # no validation on MCCSAllocation subschema
    ],
)
@vcrpy.use_cassette
def test_releaseresources_serialisation_and_validation(
    schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )

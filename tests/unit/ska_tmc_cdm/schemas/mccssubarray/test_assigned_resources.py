"""
Unit tests for ska_tmc_cdm.schemas.mccssubarray.assigned_resources module.
"""

import pytest

from ska_tmc_cdm.messages.mccssubarray.assigned_resources import AssignedResources
from ska_tmc_cdm.schemas.mccssubarray.assigned_resources import AssignedResourcesSchema
from .. import utils

VALID_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-mccs-assignedresources/1.0",
  "subarray_beam_ids": [1],
  "station_ids": [[1,2]],
  "channel_blocks": [3]
}
"""

INVALID_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-mccs-assignedresources/1.0",
  "subarray_beam_ids": [-1],
  "station_ids": [[1,2]],
  "channel_blocks": [3]
}
"""

VALID_EMPTY_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-mccs-assignedresources/1.0",
  "subarray_beam_ids": [],
  "station_ids": [],
  "channel_blocks": []
}
"""

VALID_OBJECT = AssignedResources(
    interface="https://schema.skao.int/ska-low-mccs-assignedresources/1.0",
    subarray_beam_ids=[1],
    station_ids=[[1, 2]],
    channel_blocks=[3]
)

VALID_EMPTY_OBJECT = AssignedResources(
    interface="https://schema.skao.int/ska-low-mccs-assignedresources/1.0",
    subarray_beam_ids=[],
    station_ids=[],
    channel_blocks=[]
)


@pytest.mark.parametrize(
    'schema_cls,instance,modifier_fn,valid_json,invalid_json',
    [
        (AssignedResourcesSchema,
         VALID_OBJECT,
         lambda o: setattr(o, 'subarray_beam_ids', [-1]),
         VALID_JSON,
         INVALID_JSON),
        (AssignedResourcesSchema,
         VALID_EMPTY_OBJECT,
         lambda o: setattr(o, 'subarray_beam_ids', [-1]),
         VALID_EMPTY_JSON,
         None)
    ]
)
def test_assigned_resources_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that AssignedResourcesSchema marshals, unmarshals, and validates
    correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )

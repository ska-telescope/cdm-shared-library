"""
Unit tests for the CentralNode.ReleaseResources request/response mapper
module.
"""
from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import ValidationError

from ska_tmc_cdm.messages.central_node.release_resources import SCHEMA
from tests.unit.ska_tmc_cdm.builder.central_node.release_resources import (
    ReleaseResourcesRequestBuilder,
)


@pytest.mark.parametrize(
    ("subarray_id", "okay"),
    zip(range(-5, 21), ([False] * 6 + [True] * 16 + [False] * 4)),
)
def test_validation_applies_to_subarray_id(subarray_id: int, okay: bool):
    "subarray_id must be from 1...16, inclusive"
    if okay:
        expectation = does_not_raise()
    else:
        expectation = pytest.raises(ValidationError)
    with expectation:
        ReleaseResourcesRequestBuilder(subarray_id=subarray_id)


def test_deallocate_resources_must_define_resources_if_not_releasing_all():
    """
    Verify that resource argument(s) must be set if the command is not a
    command to release all sub-array resources.
    """
    with pytest.raises(ValueError):
        ReleaseResourcesRequestBuilder(release_all=False, dish_allocation=None)

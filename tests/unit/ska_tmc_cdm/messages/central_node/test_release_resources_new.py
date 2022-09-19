"""
Unit tests to demonstrate expand pattern for a class method "from_any_schema_keyvalue"
in the CentralNode.ReleaseResources request/response mapper
module.
"""
import json

import pytest

from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.release_resources_new import (
    ReleaseResourcesRequest,
)


# Based on OET → TMC (Mid) CentralNode.AssignResources
# example JSON after ADR-3
# Here we try out a new schema :
def test_new_keyvalues_obj():
    """
        Verify that object is created successfully with entirely new key-value pairs.
    {
        "sdp_id": "sbi-mvp01-20220919-00001", // string
        "sdp_max_length": 125.40, // float
        "subbands": [0.55e9,0.95e9,186] //long,long,int
    }
    :param sdp_id: string denoting id for science data processor in use.
    :param sdp_max_length: float denoting max length required in seconds.
    :param subbands: min freq, max freq, no of channels
    """
    json_kv = '{"sdp_id":"sbi-mvp01-20220919-00001",\
                "sdp_max_length":125.40,"subbands":[0.55e9,0.95e9,186]}'
    request = ReleaseResourcesRequest(json_key_value=json_kv)

    # check whether object created with correct values
    for keys in json.loads(json_kv):
        assert (request.__dict__)[keys] == (json.loads(json_kv))[keys]


def test_altschemas_keyvalues_obj():
    """Verify that two different objects created from slightly changed layout
    but same key-value pair are identical.
    "subbands": [{"freq_min": 0.55e9,"freq_max": 0.95e9,"nchan": 186}, ...
    and also "subbands":[0.55e9,0.95e9,186] must be identical."""

    json_channel = '{"freq_min": 0.55e9,"freq_max": 0.95e9,"nchan": 186}'
    json_channel_alt = '{"subbands":[0.55e9,0.95e9,186]}'
    request1 = ReleaseResourcesRequest(json_key_value=json_channel, release_all=True)
    request2 = ReleaseResourcesRequest(
        json_key_value=json_channel_alt, release_all=True
    )
    index = 0
    for k in json.loads(json_channel):
        for k_y in json.loads(json_channel_alt):
            assert ((request2.__dict__)[k_y])[index] == (request1.__dict__)[k]
        index = index + 1


# Below we keep the existing tests as for this class method
def test_old_eq():
    """
    Verify that two ReleaseResource requests for the same sub-array and
    dish allocation are considered equal.
    Verify that two ReleaseResource requests for the same sub-array
    are considered equal.
    Verify that a ReleaseResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = ReleaseResourcesRequest(
        subarray_id=1,
        dish_allocation=dish_allocation,
        release_all=False,
        transaction_id="tma1",
    )
    assert request == ReleaseResourcesRequest(
        subarray_id=1,
        dish_allocation=dish_allocation,
        release_all=False,
        transaction_id="tma1",
    )
    assert request != ReleaseResourcesRequest(
        subarray_id=1, dish_allocation=DishAllocation(), transaction_id="tma1"
    )
    assert request != ReleaseResourcesRequest(
        subarray_id=2, dish_allocation=dish_allocation, transaction_id="tma1"
    )
    assert request != ReleaseResourcesRequest(
        subarray_id=1,
        dish_allocation=dish_allocation,
        release_all=True,
        transaction_id="tma1",
    )
    assert request != ReleaseResourcesRequest(
        subarray_id=1, dish_allocation=dish_allocation, transaction_id="blah"
    )
    assert request != ReleaseResourcesRequest(
        subarray_id=1, dish_allocation=dish_allocation
    )
    request = ReleaseResourcesRequest(subarray_id=1, release_all=True)
    assert request == ReleaseResourcesRequest(subarray_id=1, release_all=True)
    assert request != ReleaseResourcesRequest(subarray_id=2, release_all=True)
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = ReleaseResourcesRequest(subarray_id=1, dish_allocation=dish_allocation)
    assert request != 1
    assert request != object()


def test_old_value_errors():
    """
    Verify that resource argument(s) must be set if the command is not a
    command to release all sub-array resources.
    Verify that the boolean release_all_mid argument is required.
    """
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(subarray_id=1, release_all=False)
    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(
            subarray_id=1, release_all=1, dish_allocation=dish_allocation
        )

"""
Unit tests to demonstrate expand pattern i.e. support for new keywords for upcoming schemes while backward compatibility to existing/old schemas
for a class method "from_any_schema_keyvalue" in the CentralNode.ReleaseResources request/response mapper
module.
"""
import pytest

from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.release_resources import ReleaseResourcesRequest
# Here we try out a new schema :
# collected Devereux Drew's comment on Mar 22 2021 at https://confluence.skatelescope.org/display/SWSI/Configuration+Schemas#ConfigurationSchemas-OET%E2%86%92TMC(Mid):
""" {
    "subarray_id": 1,
    "station_ids": [1,2],
    "channels": [[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 1]], # [start channel, num channels, beam index, substation_id]
    "subarray_beam_ids": [1],
}"""
def test_new_keyvalues_obj():
    """
    Verify that object is created successfully with entirely new key-value pairs.
    """
    json_kv='{"subarray_id":1,"station_ids":[1,2],"channels":[[0,8,1,1],[8,8,2,1],[24,16,2,1]],"subarray_beam_ids":[1]}'
    request=ReleaseResourcesRequest.from_any_schema_keyvalue(json_keyValuePair=json_kv)

    #check whether object created with correct values
    assert request.subarray_id==1
    assert (request.station_ids[0]==1 and request.station_ids[1]==2)
    assert (len(request.channels)==3 and len(request.channels[0])==4)
    assert request.subarray_beam_ids[0]==1

def test_altschemas_keyvalues_obj():
    """Verify that two different objects created from slightly changed layout
    but same key-value pair are identical.
    channels": [{"start_channel": 0,"num_channels": 8,"beam_index": 1,"substation_id": 1}, ...
    and also "channels":[[0,8,1,1],...] must be identical."""

    json_channel='{"start_channel":0,"num_channels":8,"beam_index":1,"substation_id":1}'
    json_channel_alt='{"channels":[0,8,1,1]}'
    request1=ReleaseResourcesRequest.from_any_schema_keyvalue(json_keyValuePair=json_channel)
    request2=ReleaseResourcesRequest.from_any_schema_keyvalue(json_keyValuePair=json_channel_alt)
    assert (request1.start_channel==request2.channels[0] and request1.num_channels==request2.channels[1] and request1.beam_index==request2.channels[2] and request1.substation_id==request2.channels[3])


# Below we keep the same tests for existing scheme using class method as used when we used constructor

def test_old_eq():
    """
    Verify that two ReleaseResource requests for the same sub-array and
    dish allocation are considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = ReleaseResourcesRequest.from_any_schema_keyvalue(
        subarray_id=1,
        dish_allocation=dish_allocation,
        release_all=False,
        transaction_id="tma1",
    )
    assert request == ReleaseResourcesRequest.from_any_schema_keyvalue(
        subarray_id=1, dish_allocation=dish_allocation,release_all=False,transaction_id="tma1"
    )
    assert request != ReleaseResourcesRequest.from_any_schema_keyvalue(
        subarray_id=1, dish_allocation=DishAllocation(), transaction_id="tma1"
    )
    assert request != ReleaseResourcesRequest.from_any_schema_keyvalue(
        subarray_id=2, dish_allocation=dish_allocation, transaction_id="tma1"
    )
    assert request != ReleaseResourcesRequest.from_any_schema_keyvalue(
        subarray_id=1,
        dish_allocation=dish_allocation,
        release_all=True,
        transaction_id="tma1",
    )
    assert request != ReleaseResourcesRequest.from_any_schema_keyvalue(
        subarray_id=1, dish_allocation=dish_allocation, transaction_id="blah"
    )
    assert request != ReleaseResourcesRequest.from_any_schema_keyvalue(
        subarray_id=1, dish_allocation=dish_allocation
    )

    """
    Verify that two ReleaseResource requests for the same sub-array
    are considered equal.
    """

    request = ReleaseResourcesRequest.from_any_schema_keyvalue(subarray_id=1, release_all=True)

    assert request == ReleaseResourcesRequest.from_any_schema_keyvalue(subarray_id=1, release_all=True)
    assert request != ReleaseResourcesRequest.from_any_schema_keyvalue(subarray_id=2, release_all=True)

    """
    Verify that a ReleaseResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = ReleaseResourcesRequest.from_any_schema_keyvalue(subarray_id=1, dish_allocation=dish_allocation)
    assert request != 1
    assert request != object()

def test_old_valueErrors():
    """
    Verify that resource argument(s) must be set if the command is not a
    command to release all sub-array resources.
    """
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest.from_any_schema_keyvalue(subarray_id=1, release_all=False)

    """
    Verify that resource argument(s) must be set if the command is not a
    command to release all sub-array resources.
    """
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest.from_any_schema_keyvalue(subarray_id=1, release_all=False)

    """
    Verify that the boolean release_all_mid argument is required.
    """
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest.from_any_schema_keyvalue(subarray_id=1, release_all=1)

    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(
            subarray_id=1, release_all=1, dish_allocation=dish_allocation
        )

    # If release_all is not set as boolean for Low
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest.from_any_schema_keyvalue(subarray_id=1, release_all=1)

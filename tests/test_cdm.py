"""
Unit tests for cdm module.
"""
from cdm_lib.messages import AssignResources
from cdm_lib.schemas import Dish

VALID_ASSIGN_RESOURCES_JSON = """{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}"""

def test_asssign_resources_request():
    """Create a request string from a subarrayID and a valid dish configuration"""

    assign_resources = AssignResources(1, Dish(receptorIDList=["0001", "0002"]))
    request = repr(assign_resources)
    assert request == VALID_ASSIGN_RESOURCES_JSON

def test_parse_assign_resources():
    """Create an AssignResources object from an incomming request """
    request = AssignResources.from_request(VALID_ASSIGN_RESOURCES_JSON)
    assert request.subarray.subarrayID == 1
    assert request.subarray.dish.receptorIDList == ["0001", "0002"]

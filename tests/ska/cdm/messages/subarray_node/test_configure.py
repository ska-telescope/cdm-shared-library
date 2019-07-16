"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
from ska.cdm.messages.subarray_node.configure_subarray import ConfigureRequest,\
    Target, DishConfiguration, PointingConfiguration


# TODO
def test_configure_subarray_request_eq():

    TARGET_NAME = 'another planet';

    """
    Verify that two Configure Subarray requests with the same pointing and
    dish parameters
    """

    target = Target(ra=1.0, dec=1.0, frame="icrs", name=TARGET_NAME)
    assert target.coord.info.name ==  TARGET_NAME
    pointing  = PointingConfiguration(target)
    dish = DishConfiguration(["aa","bb"])

    request = ConfigureRequest(dish=dish, pointing=pointing)

    #TODO still need to agree if this is true
    #assert request == ConfigureRequest(dish=dish, pointing=pointing)
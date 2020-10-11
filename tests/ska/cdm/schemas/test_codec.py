"""
Unit tests for the ska.cdm.schemas.codec module.
"""
import os.path

from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska.cdm.messages.central_node.csp import DishAllocation
from ska.cdm.messages.central_node.mccs import MCCSAllocate
from ska.cdm.messages.subarray_node.configure import ConfigureRequest
from ska.cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    ReceiverBand,
)
from ska.cdm.schemas import CODEC
from .central_node.test_central_node import (
    VALID_ASSIGN_RESOURCES_REQUEST,
    sdp_config_for_test,
)
from ska.cdm.utils import json_is_equal


def test_codec_loads():
    """
    Verify that the codec unmarshalls objects correctly.
    """
    sdp_config = sdp_config_for_test()
    mccs_allocate = MCCSAllocate(1, [1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    unmarshalled = CODEC.loads(AssignResourcesRequest, VALID_ASSIGN_RESOURCES_REQUEST)
    expected = AssignResourcesRequest(
        1,
        DishAllocation(receptor_ids=["0001", "0002"]),
        sdp_config=sdp_config,
        mccs_allocate=mccs_allocate,
    )
    assert expected == unmarshalled


def test_codec_dumps():
    """
    Verify that the codec marshalls objects to JSON.
    """
    sdp_config = sdp_config_for_test()
    mccs_allocate = MCCSAllocate(1, [1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    expected = VALID_ASSIGN_RESOURCES_REQUEST
    obj = AssignResourcesRequest(
        1,
        DishAllocation(receptor_ids=["0001", "0002"]),
        sdp_config=sdp_config,
        mccs_allocate=mccs_allocate,
    )

    marshalled = CODEC.dumps(obj)
    assert json_is_equal(marshalled, expected)


def test_read_a_file_from_disk():
    """
    Test for loading a configure request from a JSON file
    """
    cwd, _ = os.path.split(__file__)
    test_data = os.path.join(cwd, "testfile_sample_configure.json")
    result = CODEC.load_from_file(ConfigureRequest, test_data)
    dish_config = DishConfiguration(ReceiverBand.BAND_1)

    assert result.dish == dish_config

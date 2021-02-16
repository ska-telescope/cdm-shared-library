"""
Unit tests for the ska.cdm.schemas.codec module.
"""
import os.path

from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska.cdm.messages.central_node.common import DishAllocation
from ska.cdm.messages.central_node.mccs import MCCSAllocate
from ska.cdm.messages.subarray_node.configure import ConfigureRequest
from ska.cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    ReceiverBand,
)
from ska.cdm.schemas import CODEC
from ska.cdm.utils import json_is_equal
from .central_node.test_central_node import (
    VALID_ASSIGN_RESOURCES_REQUEST,
    VALID_MCCS_ALLOCATE_RESOURCES_REQUEST,
    sdp_config_for_test,
)


def test_codec_loads():
    """
    Verify that the codec unmarshalls objects correctly.
    """
    sdp_config = sdp_config_for_test()
    unmarshalled = CODEC.loads(AssignResourcesRequest, VALID_ASSIGN_RESOURCES_REQUEST)
    expected = AssignResourcesRequest.from_dish(
        1, DishAllocation(receptor_ids=["0001", "0002"]), sdp_config=sdp_config,
    )
    assert expected == unmarshalled


def test_codec_loads_mccs_only():
    """
    Verify that the codec unmarshalls objects correctly.
    """
    mccs_allocate = MCCSAllocate(
        1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    unmarshalled = CODEC.loads(
        AssignResourcesRequest, VALID_MCCS_ALLOCATE_RESOURCES_REQUEST
    )
    expected = AssignResourcesRequest.from_mccs(mccs_allocate=mccs_allocate)
    assert expected == unmarshalled


def test_codec_dumps():
    """
    Verify that the codec marshalls dish & sdp objects to JSON.
    """
    sdp_config = sdp_config_for_test()
    expected = VALID_ASSIGN_RESOURCES_REQUEST
    obj = AssignResourcesRequest(
        1, DishAllocation(receptor_ids=["0001", "0002"]), sdp_config=sdp_config
    )

    marshalled = CODEC.dumps(obj)
    assert json_is_equal(marshalled, expected)


def test_codec_dumps_mccs():
    """
    Verify that the codec marshalls mccs objects to JSON.
    """
    mccs_allocate = MCCSAllocate(
        1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    expected = VALID_MCCS_ALLOCATE_RESOURCES_REQUEST
    obj = AssignResourcesRequest.from_mccs(mccs_allocate=mccs_allocate)

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

    # test_new_json_data = os.path.join(cwd, "testfile_sample_configure_ADR_18.json")
    # result_data = CODEC.load_from_file(ConfigureRequest, test_new_json_data)
    # dish_config = DishConfiguration(ReceiverBand.BAND_1)
    # assert result_data.dish == dish_config

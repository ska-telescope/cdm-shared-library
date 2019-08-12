"""
Unit tests for the ska.cdm.schemas.codec module.
"""
import os.path

from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska.cdm.messages.central_node.assign_resources import DishAllocation
from ska.cdm.messages.subarray_node.configure import ConfigureRequest
from ska.cdm.schemas import CODEC
from .test_central_node import VALID_ASSIGN_RESOURCES_REQUEST


def test_codec_loads():
    """
    Verify that the codec unmarshalls objects correctly.
    """
    unmarshalled = CODEC.loads(AssignResourcesRequest, VALID_ASSIGN_RESOURCES_REQUEST)
    expected = AssignResourcesRequest(1, DishAllocation(receptor_ids=['0001', '0002']))
    assert expected == unmarshalled


def test_codec_dumps():
    """
    Verify that the codec marshalls objects to JSON.
    """
    expected = VALID_ASSIGN_RESOURCES_REQUEST
    obj = AssignResourcesRequest(1, DishAllocation(receptor_ids=['0001', '0002']))
    marshalled = CODEC.dumps(obj)
    assert expected == marshalled


def test_read_a_file_from_disk():
    """
    Test for loading a configure request from a JSON file
    """
    cwd, _ = os.path.split(__file__)
    test_data = os.path.join(cwd, 'testfile_sample_configure.json')
    result = CODEC.load_from_file(ConfigureRequest, test_data)
    assert result.scan_id == 123

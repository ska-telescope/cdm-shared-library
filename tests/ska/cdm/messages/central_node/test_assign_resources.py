"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""

import pytest

from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest, \
    AssignResourcesResponse, DishAllocation, ProcessingBlockConfiguration, SDPWorkflow, \
    SDPConfiguration, ScanType, SubBand



def test_workflow_equals():
    """
    Verify that SDP Workflow objects are considered equal when they have:
     - the same ID
     - the same type
     - the same version
    """
    workflow1 = SDPWorkflow('id', 'type', 'version')
    workflow2 = SDPWorkflow('id', 'type', 'version')
    assert workflow1 == workflow2

    assert workflow1 != SDPWorkflow('', 'type', 'version')
    assert workflow1 != SDPWorkflow('id', '', 'version')
    assert workflow1 != SDPWorkflow('id', 'type', '')


def test_workflow_not_equal_to_other_objects():
    """
    Verify that SDP Workflow objects are not considered equal to objects of
    other types.
    """
    workflow1 = SDPWorkflow('id', 'type', 'version')
    assert workflow1 != 1


def test_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    sub_band = SubBand(0.35e9, 1.05e9, 372, [[1, 0], [101, 1]])
    scan_type = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [sub_band])
    sdp_workflow = SDPWorkflow(workflow_id="vis_receive", workflow_type="realtime", version="0.1.0")
    pb_config = ProcessingBlockConfiguration("pb-mvp01-20200325-00001", sdp_workflow, {})
    sdp_config = SDPConfiguration("sbi-mvp01-20200325-00001", 100.0, [scan_type], [pb_config])
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    request = AssignResourcesRequest(1, dish_allocation=dish_allocation, sdp_config=sdp_config)
    assert request == AssignResourcesRequest(1, dish_allocation=dish_allocation, sdp_config=sdp_config)
    assert request != AssignResourcesRequest(1, dish_allocation=dish_allocation, sdp_config=None)
    assert request != AssignResourcesRequest(1, dish_allocation=None, sdp_config=None)
    assert request != AssignResourcesRequest(2, dish_allocation=dish_allocation, sdp_config=sdp_config)


def test_assign_resources_request_eq_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    request = AssignResourcesRequest(1, dish_allocation=dish_allocation, sdp_config=None)
    assert request != 1
    assert request != object()


def test_assign_resources_response_eq():
    """
    Verify that two AssignResource response objects with the same successful
    dish allocation are considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    unequal_allocation = DishAllocation(receptor_ids=['b', 'aab'])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)

    assert response == AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response != AssignResourcesResponse(dish_allocation=DishAllocation())
    assert response != AssignResourcesResponse(dish_allocation=unequal_allocation)


def test_assign_resources_response_eq_with_other_objects():
    """
    Verify that an AssignResourcesRequest response object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response != 1
    assert response != object()


def test_dish_allocation_repr():
    """
    Verify that the DishAllocation repr is formatted correctly.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    assert repr(dish_allocation) == "<DishAllocation(receptor_ids=['ac', 'b', 'aab'])>"


def test_dish_allocation_eq():
    """
    Verify that two DishAllocations with the same allocated receptors are
    considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    assert dish_allocation == DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    assert dish_allocation == DishAllocation(receptor_ids=['b', 'ac', 'aab'])
    assert dish_allocation != DishAllocation(receptor_ids=['ac'])
    assert dish_allocation != DishAllocation(receptor_ids=['ac', 'b', 'aab', 'd'])


def test_dish_allocation_eq_with_other_objects():
    """
    Verify that a DishAllocation is considered unequal to objects of other
    types.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    assert dish_allocation != 1
    assert dish_allocation != object()


@pytest.mark.xfail
def test_marshal_sdp_configure_request():
    """
    Verify that JSON can be marshalled to JSON correctly
    """
    sb_id = 'realtime-20190627-0001'
    sbi_id = '20190627-0001'
    target = Target(ra=1.0, dec=1.0, name='NGC6251', unit='rad')
    target_list = {'0': target}

    workflow = SDPWorkflow(workflow_id='vis_ingest', workflow_type='realtime', version='0.1.0')

    parameters = SDPParameters(num_stations=4, num_channels=372,
                               num_polarisations=4, freq_start_hz=0.35e9,
                               freq_end_hz=1.05e9, target_fields=target_list)
    scan = SDPScan(field_id=0, interval_ms=1400)
    scan_list = {'12345': scan}

    pb_config = ProcessingBlockConfiguration(sb_id=sb_id,
                                             sbi_id=sbi_id,
                                             workflow=workflow,
                                             parameters=parameters,
                                             scan_parameters=scan_list)

    sdp_configure = SDPConfiguration([pb_config])
    schema = SDPConfigurationSchema()
    result = schema.dumps(sdp_configure)

    assert json_is_equal(result, VALID_SDP_CONFIGURE_SB)


@pytest.mark.xfail
def test_unmarshall_sdp_configure_request():
    """
    Verify that JSON can be unmarshalled back to an SDP SB configuration
    """
    schema = SDPConfigurationSchema()
    result = schema.loads(VALID_SDP_CONFIGURE_SB)
    config_block = result.configure[0]
    assert isinstance(config_block, ProcessingBlockConfiguration)


@pytest.mark.xfail
def test_unmarshall_both_sdp_configure_and_configure_scan_request():
    """
    Verify that SB- and scan-level configurations can be unmarshalled and
    co-exist in the same SDPConfiguration.
    """
    schema = SDPConfigurationSchema()
    result = schema.loads(VALID_SDP_CONFIGURE_AND_CONFIGURE_SCAN)
    assert isinstance(result.configure, list)
    assert isinstance(result.configure_scan, SDPScanParameters)


@pytest.mark.xfail
def test_unmarshall_empty_sdp_configure_request():
    """
    Nominal test  - more for documentation - since both configure and confgureScan are optional
    it is technically possible to have an sdp configuration that is empty.
    Placeholder for a test if we close this down.
    """
    schema = SDPConfigurationSchema()
    result = schema.loads('{}')
    assert result == SDPConfiguration()

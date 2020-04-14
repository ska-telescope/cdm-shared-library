"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""

from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest, \
    AssignResourcesResponse, DishAllocation, ProcessingBlockConfiguration, PbDependency, \
    SDPWorkflow, SDPConfiguration, ScanType, SubBand


def test_sub_band_equals():
    """
    Verify that SubBand subbdand objects are considered equal when they have the same:
     - freq_min
     - freq_max
     - nchan
     - input_link_map
    """
    sub_band1 = SubBand(0.35e9, 1.05e9, 372, [[1, 0], [101, 1]])
    sub_band2 = SubBand(0.35e9, 1.05e9, 372, [[1, 0], [101, 1]])
    assert sub_band1 == sub_band2

    assert sub_band1 != SubBand(0.35e9, 1.05e9, 362, [[1, 0], [101, 1]])
    assert sub_band1 != SubBand(0.35e9, 1.05e9, 372, [[1, 1], [101, 1]])
    assert sub_band1 != SubBand(0.35e9, 1.05e9, 372, [[1, 0], [101, 2]])


def test_sub_band_not_equal_to_other_objects():
    """
    Verify that SubBand objects are not considered equal to objects of
    other types.
    """
    sub_band = SubBand(0.35e9, 1.05e9, 372, [[1, 0], [101, 1]])
    assert sub_band != 1


def test_scan_type_equals():
    """
    Verify that ScanType objects are considered equal for the same passed parameter list
    """
    sub_band = SubBand(0.35e9, 1.05e9, 372, [[1, 0], [101, 1]])
    scan_type1 = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [sub_band])
    scan_type2 = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [sub_band])

    assert scan_type1 == scan_type2

    assert scan_type1 != ScanType("calibration_B", "ICRS", "02:42:40.771", "-00:00:47.84", None)
    assert scan_type1 != ScanType("calibration_B", "ICRS", "12:29:06.699", "02:03:08.598", None)
    assert scan_type1 != ScanType("science_A", "ICRS", "12:29:06.699", "02:03:08.598", [sub_band])


def test_scan_type_not_equal_to_other_objects():
    """
    Verify that ScanType objects are not considered equal to objects of
    other types.
    """
    sub_band = SubBand(0.35e9, 1.05e9, 372, [[1, 0], [101, 1]])
    scan_type = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [sub_band])
    assert scan_type != 1


def test_workflow_equals():
    """
    Verify that SDPWorkflow objects are considered equal when they have:
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
    Verify that SDPWorkflow objects are not considered equal to objects of
    other types.
    """
    workflow = SDPWorkflow('id', 'type', 'version')
    assert workflow != 1


def test_dependency_equals():
    """
    Verify that PBDependency objects are considered equal when they have:
     - the same PB ID
     - the same type
    """
    dep1 = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    dep2 = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])

    assert dep1 == dep2

    assert dep1 != PbDependency("pb-mvp01-20200325-00001", ["calibration"])
    assert dep1 != PbDependency("pb-mvp01-20200325-00003", ["calibration"])


def test_dependency_not_equal_to_other_objects():
    """
    Verify that PBDependency objects are not considered equal to objects of
    other types.
    """
    dep = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    assert dep != 1


def test_processing_block_equals():
    """
    Verify that ProcessingBlock objects are considered equal
    """
    w_flow = SDPWorkflow("vis_receive", "realtime", "0.1.0")
    dep = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    pb1 = ProcessingBlockConfiguration("pb-mvp01-20200325-00003", w_flow, {}, [dep])
    pb2 = ProcessingBlockConfiguration("pb-mvp01-20200325-00003", w_flow, {}, [dep])

    assert pb1 == pb2

    assert pb1 != ProcessingBlockConfiguration("pb-mvp01-20200325-00001", w_flow, {}, [dep])
    assert pb1 != ProcessingBlockConfiguration("pb-mvp01-20200325-00001", None, {}, [dep])
    assert pb1 != ProcessingBlockConfiguration("pb-mvp01-20200325-00003", w_flow, None, [dep])
    assert pb1 != ProcessingBlockConfiguration("pb-mvp01-20200325-00003", w_flow, {})


def test_processing_block_not_equal_to_other_objects():
    """
    Verify that ProcessingBlock objects are not considered equal to objects of
    other types.
    """
    p_block = ProcessingBlockConfiguration("pb-mvp01-20200325-00003", None, None, None)
    assert p_block != 1


def test_sdp_configuration_block_equals():
    """
    Verify that SDPConfiguration objects are considered equal
    """
    sub_band = SubBand(0.35e9, 1.05e9, 372, [[1, 0], [101, 1]])
    scan_type1 = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [sub_band])
    scan_type2 = ScanType("calibration_B", "ICRS", "02:42:40.771", "-00:00:47.84", [sub_band])

    scan_types = [scan_type1, scan_type2]

    wf1 = SDPWorkflow("vis_receive", "realtime", "0.1.0")
    wf2 = SDPWorkflow("test_realtime", "realtime", "0.1.0")
    wf3 = SDPWorkflow("ical", "batch", "0.1.0")
    wf4 = SDPWorkflow("dpreb", "batch", "0.1.0")

    dep1 = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    dep2 = PbDependency("pb-mvp01-20200325-00003", ["calibration"])

    pb1 = ProcessingBlockConfiguration("pb-mvp01-20200325-00001", wf1, {})
    pb2 = ProcessingBlockConfiguration("pb-mvp01-20200325-00002", wf2, {})
    pb3 = ProcessingBlockConfiguration("pb-mvp01-20200325-00003", wf3, {}, [dep1])
    pb4 = ProcessingBlockConfiguration("pb-mvp01-20200325-00004", wf4, {}, [dep2])

    processing_blocks = [pb1, pb2, pb3, pb4]

    sdp1 = SDPConfiguration("sbi-mvp01-20200325-00001", 100.0, scan_types, processing_blocks)
    sdp2 = SDPConfiguration("sbi-mvp01-20200325-00001", 100.0, scan_types, processing_blocks)

    assert sdp1 == sdp2

    assert sdp1 != SDPConfiguration("sbi-mvp01-20200325-00001", 0.0, scan_types, processing_blocks)
    assert sdp1 != SDPConfiguration("sbi-mvp01-20200325-00001", 100.0, None, processing_blocks)
    assert sdp1 != SDPConfiguration("sbi-mvp01-20200325-00002", 100.0, scan_types, None)
    assert sdp1 != SDPConfiguration(None, None, None, None)


def test_sdp_configuration_not_equal_to_other_objects():
    """
    Verify that SDPConfiguration objects are not considered equal to objects of
    other types.
    """
    sdp = SDPConfiguration(None ,None, None, None)
    assert sdp != 1


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

    assert request == AssignResourcesRequest(1, dish_allocation=dish_allocation, 
                                             sdp_config=sdp_config)

    assert request != AssignResourcesRequest(1, dish_allocation=dish_allocation, sdp_config=None)
    assert request != AssignResourcesRequest(1, dish_allocation=None, sdp_config=None)
    assert request != AssignResourcesRequest(1, dish_allocation=None, sdp_config=sdp_config)


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

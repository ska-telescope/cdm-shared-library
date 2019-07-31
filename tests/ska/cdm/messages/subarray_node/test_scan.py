"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import datetime
from ska.cdm.messages.subarray_node.scan import ScanRequest

def test_scan_request_init():
    """
    Create a ScanRequest instance with a 10s timedelta and verify
    __eq__ methods

    :return: true if the object created has the same scan_duration
    """
    first_date = '2019-01-01 08:00:00.000000'
    first_date_obj = datetime.datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S.%f')

    second_date = '2019-01-01 08:00:00.000000'
    second_date_obj = datetime.datetime.strptime(second_date, '%Y-%m-%d %H:%M:%S.%f')

    t_to_scan = second_date_obj - first_date_obj
    scan_request = ScanRequest(t_to_scan)
    scan_request_2 = ScanRequest(t_to_scan)

    empty_object = ""

    assert scan_request.scan_duration == t_to_scan
    assert scan_request != empty_object

    #equal if the contents are identical
    assert scan_request == scan_request_2

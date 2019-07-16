"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
from ska.cdm.messages.subarray_node.scan import ScanRequest
from datetime import timedelta
import datetime

def test_scan_request_init():
    first_date = '2019-01-01 08:00:00.000000'
    first_date_obj = datetime.datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S.%f')

    second_date = '2019-01-01 08:00:00.000000'
    second_date_obj = datetime.datetime.strptime(second_date, '%Y-%m-%d %H:%M:%S.%f')

    t = second_date_obj - first_date_obj
    scan_request = ScanRequest(t)
    assert scan_request.scan_duration == t


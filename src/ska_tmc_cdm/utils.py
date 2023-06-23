"""
Utilities for ska_tmc_cdm.schemas tests.
"""
import json

from deepdiff import DeepDiff


def assert_json_is_equal(json_a, json_b):
    """
    Utility function to compare two JSON objects
    """
    # key/values in the generated JSON do not necessarily have the same order
    # as the test string, even though they are equivalent JSON objects, e.g.,
    # subarray_id could be defined after dish. Ensure a stable test by
    # comparing the JSON objects themselves.
    a = json.loads(json_a)
    b = json.loads(json_b)
   
    try:
        assert a == b
    except AssertionError as e:
        # raise a more useful exception that shows *where* the JSON differs
        diff = DeepDiff(a, b, ignore_order=True)
        raise AssertionError(f"JSON not equal: {diff}") from e

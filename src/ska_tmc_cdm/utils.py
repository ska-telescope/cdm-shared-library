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
    alpha = json.loads(json_a)
    beta = json.loads(json_b)
    # Prettier diffs that are easier to read:
    if diff := DeepDiff(alpha, beta, ignore_order=True):
        raise AssertionError(f"JSON not equal: {diff}")

"""
Utilities for ska.cdm.schemas tests.
"""
import json


def json_is_equal(json_a, json_b):
    """
    Utility function to compare two JSON objects
    """
    # key/values in the generated JSON do not necessarily have the same order
    # as the test string, even though they are equivalent JSON objects, e.g.,
    # subarrayID could be defined after dish. Ensure a stable test by
    # comparing the JSON objects themselves.
    return json.loads(json_a) == json.loads(json_b)

"""
Unit tests for the ska_tmc_cdm.jsonschema.json_schema module.
"""
import copy

import pytest
from ska_telmodel.tmc.examples import TMC_LOW_RELEASERES_1_0 as VALID_JSON

from ska_tmc_cdm.jsonschema.json_schema import (
    JsonSchema,
    JsonValidationError,
    SchemaNotFound
)

INVALID_JSON = copy.deepcopy(VALID_JSON)
INVALID_JSON["release_all"] = "foo"


def test_schema_validation_with_valid_json():
    """
    Verify schema validation with test valid json
    """
    json_schema_obj = JsonSchema()
    json_schema_obj.validate_schema(uri=VALID_JSON["interface"],
                                    instance=VALID_JSON)


def test_schema_validation_with_invalid_json():
    """
    Verify schema validation where interface uri is specified with wrong
    version number
    """
    json_schema_obj = JsonSchema()
    with pytest.raises(JsonValidationError):
        json_schema_obj.validate_schema(uri=INVALID_JSON["interface"],
                                        instance=INVALID_JSON)


def test_schema_with_invalid_schema_uri():
    """
    Verify schema with invalid uri raise exception
    """
    json_schema_obj = JsonSchema()

    with pytest.raises(SchemaNotFound):
        json_schema_obj.get_schema_by_uri(uri="https://foo.com/badschema/1.0")

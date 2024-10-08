"""
Unit tests for the ska_tmc_cdm.jsonschema.json_schema module.
"""
import copy
import json

import pytest
from ska_ost_osd.telvalidation.semantic_validator import (
    SchematicValidationError,
)

from ska_tmc_cdm.jsonschema.json_schema import (
    JsonSchema,
    JsonValidationError,
    SchemaNotFound,
)
from tests.unit.ska_tmc_cdm.serialisation.central_node.test_assign_resources import (
    INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
    INVALID_MID_ASSIGNRESOURCESREQUEST_JSON,
    VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
    VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16,
)
from tests.unit.ska_tmc_cdm.serialisation.subarray_node.test_configure import (
    INVALID_LOW_CONFIGURE_JSON,
    VALID_LOW_CONFIGURE_JSON,
)

VALID_JSON = {
    "interface": "https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0",
    "subarray_id": 1,
    "release_all": True,
}

INVALID_JSON = copy.deepcopy(VALID_JSON)
INVALID_JSON["release_all"] = "foo"


def test_schema_validation_with_valid_json():
    """
    Verify schema validation with test valid json
    """
    json_schema_obj = JsonSchema()
    json_schema_obj.validate_schema(
        uri=VALID_JSON["interface"], instance=VALID_JSON
    )


def test_schema_validation_with_invalid_json():
    """
    Verify schema validation where interface uri is specified with wrong
    version number
    """
    json_schema_obj = JsonSchema()
    with pytest.raises(JsonValidationError):
        json_schema_obj.validate_schema(
            uri=INVALID_JSON["interface"], instance=INVALID_JSON
        )


def test_schema_with_invalid_schema_uri():
    """
    Verify schema with invalid uri raise exception
    """
    json_schema_obj = JsonSchema()

    with pytest.raises(SchemaNotFound):
        json_schema_obj.get_schema_by_uri(uri="https://foo.com/badschema/1.0")


def test_semantic_validation_with_valid_json():
    """
    Verify semantic validation with test valid json
    """
    MID_VALID_JSON = json.loads(VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16)
    json_schema_obj = JsonSchema()
    json_schema_obj.semantic_validate_schema(
        instance=MID_VALID_JSON, uri=MID_VALID_JSON["interface"]
    )


def test_semantic_validation_with_invalid_json():
    """
    Verify semantic validation with test invalid json
    """
    MID_INVALID_JSON = json.loads(INVALID_MID_ASSIGNRESOURCESREQUEST_JSON)
    json_schema_obj = JsonSchema()
    with pytest.raises(SchematicValidationError):
        json_schema_obj.semantic_validate_schema(
            instance=MID_INVALID_JSON, uri=MID_INVALID_JSON["interface"]
        )


def test_semantic_validation_low_tmc_assign_with_valid_json():
    """
    Verify semantic validation with test low assign resources valid json
    """
    LOW_ASSIGN_VALID_JSON = json.loads(VALID_LOW_ASSIGNRESOURCESREQUEST_JSON)
    json_schema_obj = JsonSchema()
    result = json_schema_obj.semantic_validate_schema(
        instance=LOW_ASSIGN_VALID_JSON, uri=LOW_ASSIGN_VALID_JSON["interface"]
    )
    assert result


def test_semantic_validation_low_tmc_assign_with_invalid_json():
    """
    Verify semantic validation with test low assign resources invalid json
    """
    LOW_ASSIGN_INVALID_JSON = json.loads(
        INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON
    )
    json_schema_obj = JsonSchema()

    with pytest.raises(SchematicValidationError):
        json_schema_obj.semantic_validate_schema(
            instance=LOW_ASSIGN_INVALID_JSON,
            uri=LOW_ASSIGN_INVALID_JSON["interface"],
        )


def test_semantic_validation_low_tmc_configure_with_valid_json():
    """
    Verify semantic validation with test low configure valid json
    """
    LOW_CONFIGURE_VALID_JSON = json.loads(VALID_LOW_CONFIGURE_JSON)
    json_schema_obj = JsonSchema()
    result = json_schema_obj.semantic_validate_schema(
        instance=LOW_CONFIGURE_VALID_JSON,
        uri=LOW_CONFIGURE_VALID_JSON["interface"],
    )
    assert result


def test_semantic_validation_low_tmc_configure_with_invalid_json():
    """
    Verify semantic validation with test low configure invalid json
    """
    LOW_CONFIGURE_INVALID_JSON = json.loads(INVALID_LOW_CONFIGURE_JSON)
    json_schema_obj = JsonSchema()

    with pytest.raises(SchematicValidationError):
        json_schema_obj.semantic_validate_schema(
            instance=LOW_CONFIGURE_INVALID_JSON,
            uri=LOW_CONFIGURE_INVALID_JSON["interface"],
        )


def test_semantic_validation_low_tmc_configure_3_2_with_invalid_json():
    """
    Verify semantic validation with test low configure 3.2 schema invalid json
    """
    LOW_CONFIGURE_INVALID_JSON = json.loads(INVALID_LOW_CONFIGURE_JSON)
    json_schema_obj = JsonSchema()

    with pytest.raises(SchematicValidationError):
        json_schema_obj.semantic_validate_schema(
            instance=LOW_CONFIGURE_INVALID_JSON,
            uri=LOW_CONFIGURE_INVALID_JSON["interface"],
        )

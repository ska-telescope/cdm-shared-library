"""
Unit tests for the ska_tmc_cdm.schemas.codec module.
"""
import json
import tempfile
from contextlib import nullcontext as does_not_raise

import pytest
from ska_ost_osd.telvalidation.semantic_validator import (
    SchematicValidationError,
)

from ska_tmc_cdm.exceptions import JsonValidationError, SchemaNotFound
from ska_tmc_cdm.messages.central_node.assign_resources import (
    AssignResourcesRequest,
)
from ska_tmc_cdm.messages.central_node.release_resources import (
    ReleaseResourcesRequest,
)
from ska_tmc_cdm.messages.subarray_node.configure import ConfigureRequest
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.schemas.telmodel_validation import SEMANTIC_VALIDATION
from ska_tmc_cdm.utils import assert_json_is_equal
from tests.unit.ska_tmc_cdm.serialisation.central_node.test_assign_resources import (
    INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
    INVALID_MID_ASSIGNRESOURCESREQUEST_JSON,
    VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
    VALID_LOW_ASSIGNRESOURCESREQUEST_JSON_4_0,
    VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
    VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT_4_0,
    VALID_MID_ASSIGNRESOURCESREQUEST_JSON,
    VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16,
    VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT,
    VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT_PI16,
)
from tests.unit.ska_tmc_cdm.serialisation.central_node.test_release_resources import (
    VALID_LOW_FULL_RELEASE_JSON,
    VALID_LOW_FULL_RELEASE_OBJECT,
    VALID_MID_FULL_RELEASE_JSON,
    VALID_MID_FULL_RELEASE_OBJECT,
)
from tests.unit.ska_tmc_cdm.serialisation.subarray_node.test_configure import (
    INVALID_LOW_CONFIGURE_JSON,
    NON_COMPLIANCE_MID_CONFIGURE_JSON,
    VALID_LOW_CONFIGURE_JSON,
    VALID_LOW_CONFIGURE_JSON_4_0,
    VALID_LOW_CONFIGURE_OBJECT,
    VALID_LOW_CONFIGURE_OBJECT_3_1,
    VALID_LOW_CONFIGURE_OBJECT_4_0,
    VALID_MID_CONFIGURE_JSON_2_3,
    VALID_MID_CONFIGURE_OBJECT_2_3,
)

TEST_PARAMETERS = [
    (
        AssignResourcesRequest,
        VALID_MID_ASSIGNRESOURCESREQUEST_JSON,
        VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT,
        False,
    ),
    (
        AssignResourcesRequest,
        VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
        VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
        True,
    ),
    (
        AssignResourcesRequest,
        VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16,
        VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT_PI16,
        False,
    ),
    (
        ConfigureRequest,
        VALID_MID_CONFIGURE_JSON_2_3,
        VALID_MID_CONFIGURE_OBJECT_2_3,
        True,
    ),
    (
        ConfigureRequest,
        VALID_LOW_CONFIGURE_JSON,
        VALID_LOW_CONFIGURE_OBJECT,
        True,
    ),
    (
        ConfigureRequest,
        VALID_LOW_CONFIGURE_JSON_4_0,
        VALID_LOW_CONFIGURE_OBJECT_4_0,
        True,
    ),
    (
        ReleaseResourcesRequest,
        VALID_MID_FULL_RELEASE_JSON,
        VALID_MID_FULL_RELEASE_OBJECT,
        True,
    ),
    (
        ReleaseResourcesRequest,
        VALID_LOW_FULL_RELEASE_JSON,
        VALID_LOW_FULL_RELEASE_OBJECT,
        False,
    ),
    (
        AssignResourcesRequest,
        VALID_LOW_ASSIGNRESOURCESREQUEST_JSON_4_0,
        VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT_4_0,
        True,
    ),
]


@pytest.mark.parametrize(
    "msg_cls,json_str,expected, is_validate", TEST_PARAMETERS
)
def test_codec_loads(msg_cls, json_str, expected, is_validate):
    """
    Verify that the codec unmarshalls objects correctly.
    """
    unmarshalled = CODEC.loads(msg_cls, json_str, validate=is_validate)
    assert unmarshalled == expected


@pytest.mark.parametrize(
    "msg_cls,expected,instance, is_validate", TEST_PARAMETERS
)
def test_codec_dumps(
    msg_cls, expected, instance, is_validate
):  # pylint: disable=unused-argument
    """
    Verify that the codec unmarshalls objects correctly.
    """
    marshalled = CODEC.dumps(instance, validate=is_validate)
    assert_json_is_equal(marshalled, expected)


@pytest.mark.parametrize(
    "msg_cls,json_str,expected, is_validate", TEST_PARAMETERS
)
def test_codec_load_from_file(msg_cls, json_str, expected, is_validate):
    """
    Verify that the codec loads JSON from file for all key objects.
    """
    # mode='w' is required otherwise tempfile expects bytes
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write(json_str)
        f.flush()
        unmarshalled = CODEC.load_from_file(
            msg_cls, f.name, validate=is_validate
        )
        assert unmarshalled == expected


def test_codec_loads_raises_exception_on_invalid_schema():
    """
    Verify that loading data that references an invalid schema raises
    SchemaNotFound when strictness=2.
    """
    # create some test JSON that references an invalid schema
    invalid_data = json.loads(VALID_LOW_CONFIGURE_JSON)
    invalid_data["interface"] = "https://foo.com/badschema/2.0"
    invalid_data = json.dumps(invalid_data)

    strict = 2

    with pytest.raises(SchemaNotFound):
        CODEC.loads(ConfigureRequest, invalid_data, strictness=strict)

    invalid_json = json.loads(INVALID_MID_ASSIGNRESOURCESREQUEST_JSON)
    invalid_json_assign_resources = json.dumps(invalid_json)

    if SEMANTIC_VALIDATION == "true":
        with pytest.raises((SchematicValidationError, JsonValidationError)):
            CODEC.loads(
                AssignResourcesRequest,
                invalid_json_assign_resources,
                strictness=strict,
            )

    invalid_json = json.loads(NON_COMPLIANCE_MID_CONFIGURE_JSON)
    invalid_json_configure = json.dumps(invalid_json)

    if SEMANTIC_VALIDATION == "true":
        with pytest.raises((SchematicValidationError, JsonValidationError)):
            CODEC.loads(
                ConfigureRequest, invalid_json_configure, strictness=strict
            )

    invalid_json = json.loads(INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON)
    invalid_json_assign_resources = json.dumps(invalid_json)

    if SEMANTIC_VALIDATION == "true":
        with pytest.raises((SchematicValidationError, JsonValidationError)):
            CODEC.loads(
                AssignResourcesRequest,
                invalid_json_assign_resources,
                strictness=strict,
            )

    invalid_json = json.loads(INVALID_LOW_CONFIGURE_JSON)
    invalid_json["csp"]["lowcbf"]["stations"]["stn_beams"][0][
        "delay_poly"
    ] = "tango://delays.skao.int/low/stn-beam/1"
    invalid_json_configure = json.dumps(invalid_json)

    if SEMANTIC_VALIDATION == "true":
        with pytest.raises((SchematicValidationError, JsonValidationError)):
            CODEC.loads(
                ConfigureRequest, invalid_json_configure, strictness=strict
            )


def test_codec_dumps_raises_exception_on_invalid_schema():
    """
    Verify that dumping data that references an invalid schema raises
    SchemaNotFound when strictness=2.
    """
    # create a test object that references an invalid schema
    invalid_data = VALID_LOW_CONFIGURE_OBJECT_3_1.model_copy(deep=True)
    invalid_data.interface = "https://foo.com/badschema/2.0"
    # only raised when strictness=2
    CODEC.dumps(invalid_data, strictness=0)
    CODEC.dumps(invalid_data, strictness=1)
    with pytest.raises(SchemaNotFound):
        CODEC.dumps(invalid_data, strictness=2)


@pytest.mark.parametrize(
    "strictness,expectation",
    [
        (0, does_not_raise()),
        (1, does_not_raise()),
        (2, pytest.raises(JsonValidationError)),
    ],
)
def test_exception_handling_strictness_with_syntactically_invalid_json(
    caplog, strictness, expectation
):
    """
    Verify that the strictness argument is respected when loading
    syntactically invalid JSON, resulting in:

      - warning only with strictness=0,1
      - JsonValidationError with strictness=2.
    """
    request = CODEC.loads(ConfigureRequest, VALID_LOW_CONFIGURE_JSON)
    request.csp.common.subarray_id = -1

    with expectation:
        CODEC.loads(
            ConfigureRequest,
            CODEC.dumps(request),
            validate=True,
            strictness=strictness,
        )
        # note: if exception raised, this will not be asserted
        assert "WARNING" in caplog.text


@pytest.mark.parametrize("strictness", [0, 1, 2])
def test_loads_invalid_json_with_validation_disabled(strictness):
    """
    Verify that the invalid JSON can be loaded when validation is disabled.
    """
    unmarshalled = CODEC.loads(
        ConfigureRequest,
        INVALID_LOW_CONFIGURE_JSON,
        validate=False,
        strictness=strictness,
    )
    marshalled = CODEC.dumps(unmarshalled, validate=False)
    assert_json_is_equal(INVALID_LOW_CONFIGURE_JSON, marshalled)

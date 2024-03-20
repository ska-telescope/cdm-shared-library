"""
Unit tests for the ska_tmc_cdm.schemas.codec module.
"""
import copy
import functools
import json
import tempfile

import pytest

import ska_tmc_cdm
from ska_telmodel.telvalidation.semantic_validator import SchematicValidationError
from ska_tmc_cdm.exceptions import JsonValidationError, SchemaNotFound
from ska_tmc_cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska_tmc_cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska_tmc_cdm.messages.subarray_node.configure import ConfigureRequest
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.utils import assert_json_is_equal
from tests.unit.ska_tmc_cdm.schemas.central_node.test_assign_resources import (
    INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
    INVALID_MID_ASSIGNRESOURCESREQUEST_JSON,
    VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
    VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
    VALID_MID_ASSIGNRESOURCESREQUEST_JSON,
    VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16,
    VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT,
    VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT_PI16,
)
from tests.unit.ska_tmc_cdm.schemas.central_node.test_release_resources import (
    VALID_LOW_FULL_RELEASE_JSON,
    VALID_LOW_FULL_RELEASE_OBJECT,
    VALID_MID_FULL_RELEASE_JSON,
    VALID_MID_FULL_RELEASE_OBJECT,
)
from tests.unit.ska_tmc_cdm.schemas.subarray_node.test_configure import (
    INVALID_LOW_CONFIGURE_JSON,
    NON_COMPLIANCE_MID_CONFIGURE_JSON,
    VALID_LOW_CONFIGURE_3_2_JSON,
    VALID_LOW_CONFIGURE_3_2_OBJECT,
    VALID_LOW_CONFIGURE_JSON,
    VALID_LOW_CONFIGURE_OBJECT,
    VALID_MID_CONFIGURE_JSON,
    VALID_MID_CONFIGURE_OBJECT,
)

TEST_PARAMETERS = [
    # (
    #     AssignResourcesRequest,
    #     VALID_MID_ASSIGNRESOURCESREQUEST_JSON,
    #     VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT,
    #     False,
    # ),
    # (
    #     AssignResourcesRequest,
    #     VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
    #     VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
    #     True,
    # ),
    # (
    #     AssignResourcesRequest,
    #     VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16,
    #     VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT_PI16,
    #     False,
    # ),
    # (
    #     ConfigureRequest,
    #     VALID_MID_CONFIGURE_JSON,
    #     VALID_MID_CONFIGURE_OBJECT,
    #     True,
    # ),
    # (
    #     ConfigureRequest,
    #     VALID_LOW_CONFIGURE_JSON,
    #     VALID_LOW_CONFIGURE_OBJECT,
    #     True,
    # ),
    # (
    #     ReleaseResourcesRequest,
    #     VALID_MID_FULL_RELEASE_JSON,
    #     VALID_MID_FULL_RELEASE_OBJECT,
    #     True,
    # ),
    (
        ReleaseResourcesRequest,
        VALID_LOW_FULL_RELEASE_JSON,
        VALID_LOW_FULL_RELEASE_OBJECT,
        False,
    ),
    # (
    #     ConfigureRequest,
    #     VALID_LOW_CONFIGURE_3_2_JSON,
    #     VALID_LOW_CONFIGURE_3_2_OBJECT,
    #     True,
    # ),
]


@pytest.mark.trial
@pytest.mark.parametrize("msg_cls,json_str,expected, is_validate", TEST_PARAMETERS)
def test_codec_loads(msg_cls, json_str, expected, is_validate):
    """
    Verify that the codec unmarshalls objects correctly.
    """
    unmarshalled = CODEC.loads(msg_cls, json_str, validate=is_validate)
    print("unmarshalled:::::::::::", unmarshalled)
    assert unmarshalled == expected


@pytest.mark.parametrize("msg_cls,expected,instance, is_validate", TEST_PARAMETERS)
def test_codec_dumps(
    msg_cls, expected, instance, is_validate
):  # pylint: disable=unused-argument
    """
    Verify that the codec unmarshalls objects correctly.
    """
    marshalled = CODEC.dumps(instance, validate=is_validate)
    assert_json_is_equal(marshalled, expected)


@pytest.mark.parametrize("msg_cls,json_str,expected, is_validate", TEST_PARAMETERS)
def test_codec_load_from_file(msg_cls, json_str, expected, is_validate):
    """
    Verify that the codec loads JSON from file for all key objects.
    """
    # mode='w' is required otherwise tempfile expects bytes
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write(json_str)
        f.flush()
        unmarshalled = CODEC.load_from_file(msg_cls, f.name, validate=is_validate)
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

    with pytest.raises(SchemaNotFound):
        CODEC.loads(ConfigureRequest, invalid_data, strictness=2)

    invalid_json = json.loads(INVALID_MID_ASSIGNRESOURCESREQUEST_JSON)
    invalid_json_assign_resources = json.dumps(invalid_json)

    try:
        CODEC.loads(AssignResourcesRequest, invalid_json_assign_resources)
    except SchematicValidationError as error:
        assert error.message == (
            "receptor_ids are too many!Current Limit is 4\n"
            "beams are too many! Current limit is 1\n"
            "Invalid function for beams! Currently allowed visibilities\n"
            "spectral windows are too many! Current limit = 1\n"
            "Invalid input for channel_count! Currently allowed 14880\n"
            "Invalid input for freq_min\n"
            "Invalid input for freq_max\n"
            "freq_min should be less than freq_max\n"
            "length of receptor_ids should be same as length of receptors\n"
            "receptor_ids did not match receptors"
        )

    invalid_json = json.loads(NON_COMPLIANCE_MID_CONFIGURE_JSON)
    invalid_json_configure = json.dumps(invalid_json)

    try:
        CODEC.loads(ConfigureRequest, invalid_json_configure)
    except SchematicValidationError as error:
        assert error.message == (
            "Invalid input for receiver_band! Currently allowed [1,2]\n"
            "FSPs are too many!Current Limit = 4\n"
            "Invalid input for fsp_id!\n"
            "Invalid input for function_mode\n"
            "Invalid input for zoom_factor\n"
            "frequency_slice_id did not match fsp_id\n"
            "frequency_band did not match receiver_band"
        )

    invalid_json = json.loads(INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON)
    invalid_json_assign_resources = json.dumps(invalid_json)

    try:
        CODEC.loads(AssignResourcesRequest, invalid_json_assign_resources)
    except SchematicValidationError as error:
        assert error.message == (
            "beams are too many! Current limit is 1\n"
            "Invalid function for beams! Currently allowed visibilities\n"
            "spectral windows are too many! Current limit = 1"
        )

    invalid_json = json.loads(INVALID_LOW_CONFIGURE_JSON)
    invalid_json_configure = json.dumps(invalid_json)

    try:
        CODEC.loads(ConfigureRequest, invalid_json_configure)
    except SchematicValidationError as error:
        assert error.message == (
            "stations are too many! Current limit is 6\n"
            "Invalid input for function mode! Currently allowed vis\n"
            "The fsp_ids should all be distinct\n"
            "fsp_ids are too many!Current Limit is 6"
        )


def test_codec_dumps_raises_exception_on_invalid_schema():
    """
    Verify that dumping data that references an invalid schema raises
    SchemaNotFound when strictness=2.
    """
    # create a test object that references an invalid schema
    invalid_data = copy.deepcopy(VALID_LOW_CONFIGURE_OBJECT)
    invalid_data.interface = "https://foo.com/badschema/2.0"

    # validation should occur regardless of strictness, but exceptions are
    # only raised when strictness=2

    CODEC.dumps(invalid_data, strictness=0)
    CODEC.dumps(invalid_data, strictness=1)
    with pytest.raises(SchemaNotFound):
        CODEC.dumps(invalid_data, strictness=2)


def test_loads_invalid_json_with_validation_enabled():
    """
    Verify that the strictness argument is respected when loading invalid
    JSON, resulting in a JsonValidationError with strictness=2.
    """
    test_call = functools.partial(
        CODEC.loads, ConfigureRequest, INVALID_LOW_CONFIGURE_JSON, validate=True
    )

    # no exception should be raised unless strictness is 0 or 1
    for strictness in [0, 1]:
        unmarshalled = test_call(strictness=strictness, validate=False)
        marshalled = CODEC.dumps(unmarshalled, validate=False)
        assert_json_is_equal(INVALID_LOW_CONFIGURE_JSON, marshalled)

    # strictness=2 should result in an error
    with pytest.raises(JsonValidationError):
        test_call(strictness=2)


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


@pytest.mark.parametrize(
    "message_cls",
    [
        ska_tmc_cdm.messages.central_node.assign_resources.AssignResourcesRequest,
        ska_tmc_cdm.messages.central_node.assign_resources.AssignResourcesResponse,
        ska_tmc_cdm.messages.central_node.release_resources.ReleaseResourcesRequest,
        ska_tmc_cdm.messages.subarray_node.configure.ConfigureRequest,
        ska_tmc_cdm.messages.subarray_node.scan.ScanRequest,
        ska_tmc_cdm.messages.subarray_node.assigned_resources.AssignedResources,
        ska_tmc_cdm.messages.mccscontroller.allocate.AllocateRequest,
        ska_tmc_cdm.messages.mccscontroller.releaseresources.ReleaseResourcesRequest,
        ska_tmc_cdm.messages.mccssubarray.configure.ConfigureRequest,
        ska_tmc_cdm.messages.mccssubarray.scan.ScanRequest,
        ska_tmc_cdm.messages.mccssubarray.assigned_resources.AssignedResources,
    ],
)
def test_schema_registration(message_cls):
    """
    Verify that a schema is registered with the MarshmallowCodec.
    """
    assert message_cls in CODEC._schema  # pylint: disable=protected-access

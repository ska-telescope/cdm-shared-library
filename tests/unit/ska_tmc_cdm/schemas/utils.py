import copy

import pytest

from ska_tmc_cdm.exceptions import JsonValidationError, SchemaNotFound
from ska_tmc_cdm.schemas.shared import ValidatingSchema
from ska_tmc_cdm.utils import assert_json_is_equal


def test_schema_serialisation_and_validation(
    schema_cls, instance, modifier_fn, valid_json, invalid_json, is_validate=True
):
    """
    Performs a set of tests to confirm that the Marshmallow schema validates
    objects and JSON correctly when marshaling objects to JSON and when
    unmarshaling JSON to objects.

    :param schema_cls: Marshmallow schema class for object type
    :param instance: a valid instance of the object type
    :param modifier_fn: function to make the valid object invalid, or
        None if validate-on-marshal tests should be skipped
    :param valid_json: JSON equivalent of the valid instance
    :param invalid_json: invalid JSON representation, on None if
        validate-on-unmarshal tests should be skipped
    :param is_validate: Boolean True to Validate the schema, on False if
        schema validation should be skipped
    """
    test_marshal(schema_cls, instance, valid_json, is_validate)
    test_unmarshal(schema_cls, valid_json, instance, is_validate)
    test_serialising_valid_object_does_not_raise_exception_when_strict(
        schema_cls, instance, is_validate
    )

    # not all schema have validation, such as TMC MID at time of writing
    if modifier_fn is not None:

        test_serialising_invalid_object_raises_exception_when_strict(
            schema_cls, instance, modifier_fn, is_validate
        )

    # Empty instances such as '{}' do not have an invalid representation
    if invalid_json is not None:
        test_deserialising_invalid_json_raises_exception_when_strict(
            schema_cls, invalid_json, is_validate
        )


def test_marshal(schema_cls, instance, valid_json, is_validate=True):
    """
    Verify that an object instance is marshalled to JSON correctly.
    """
    # schema with strictness=1 is used so that marshalling continues when
    # SchemaNotFound is raised
    schema = get_schema(schema_cls, is_validate, strictness=1)
    marshalled = schema.dumps(instance)
    assert_json_is_equal(marshalled, valid_json)


def test_unmarshal(schema_cls, valid_json, instance, is_validate=True):
    """
    Verify that JSON is correctly unmarshalled to the expected instance.
    """
    # schema with strictness=1 is used so that marshalling continues when
    # SchemaNotFound is raised
    schema = get_schema(schema_cls, is_validate, strictness=1)
    unmarshalled = schema.loads(valid_json)
    assert unmarshalled == instance


def test_deserialising_invalid_json_raises_exception_when_strict(
    schema_cls, invalid_json, is_validate=True
):
    """
    Verifies that unmarshaling an invalid JSON string results in an exception
    when the schema validation is set to strict.

    :param schema_cls: Marshmallow schema class for object type
    :param invalid_json: JSON string
    """
    schema = get_schema(schema_cls, is_validate, strictness=2)
    with pytest.raises(JsonValidationError):
        _ = schema.loads(invalid_json)


def test_serialising_valid_object_does_not_raise_exception_when_strict(
    schema_cls, instance, is_validate=True
):
    """
    Verifies that marshaling a valid instance does not result in a validation
    error when the schema exists and schema validation is set to strict.

    :param schema_cls: Marshmallow schema class for object type
    :param instance: valid object
    """
    schema = get_schema(schema_cls, is_validate, strictness=2)
    try:
        _ = schema.dumps(instance)
    except SchemaNotFound:
        pass


def test_serialising_invalid_object_raises_exception_when_strict(
    schema_cls, instance, modifier_fn, is_validate=True
):
    """
    Verify that marshaling an invalid object results in a validation error
    when schema validation is set to strict.

    :param instance: valid object
    :param modifier_fn: function that makes the valid object invalid
    :param schema_cls: Marshmallow schema class
    """

    o = copy.deepcopy(instance)
    modifier_fn(o)

    schema = get_schema(schema_cls, is_validate, strictness=2)

    with pytest.raises(JsonValidationError):
        _ = schema.dumps(o)


def get_schema(schema_cls, is_validate=True, is_semantic_validate=False, strictness: int = 0):
    schema = schema_cls()
    schema.context[ValidatingSchema.SEMANTIC_VALIDATE] = is_semantic_validate
    schema.context[ValidatingSchema.VALIDATE] = is_validate
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = strictness
    return schema

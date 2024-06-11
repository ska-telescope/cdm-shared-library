import copy
from typing import Callable, Type

import pytest

from ska_tmc_cdm import CdmObject
from ska_tmc_cdm.exceptions import JsonValidationError, SchemaNotFound
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.utils import assert_json_is_equal

ModifierType = Callable[[CdmObject]]

def test_schema_serialisation_and_validation(
    model_class: Type[CdmObject],
    instance: CdmObject,
    modifier_fn: ModifierType,
    valid_json: str,
    invalid_json: str,
):
    """
    Performs a set of tests to confirm that the Marshmallow schema validates
    objects and JSON correctly when marshaling objects to JSON and when
    unmarshaling JSON to objects.

    :param model_class: CdmObject subclass for object type
    :param instance: a valid instance of the object type
    :param modifier_fn: function to make the valid object invalid, or
        None if validate-on-marshal tests should be skipped
    :param valid_json: JSON equivalent of the valid instance
    :param invalid_json: invalid JSON representation, on None if
        validate-on-unmarshal tests should be skipped
    :param is_validate: Boolean True to Validate the schema, on False if
        schema validation should be skipped
    """
    test_marshal(instance, valid_json)
    test_unmarshal(model_class, valid_json, instance)
    test_serialising_valid_object_does_not_raise_exception_when_strict(
        model_class,
        instance,
    )

    # not all schema have validation, such as TMC MID at time of writing
    if modifier_fn is not None:

        test_serialising_invalid_object_raises_exception_when_strict(
            model_class,
            instance,
            modifier_fn,
        )

    # Empty instances such as '{}' do not have an invalid representation
    if invalid_json is not None:
        test_deserialising_invalid_json_raises_exception_when_strict(
            model_class,
            invalid_json,
        )


def test_marshal(
    instance: CdmObject,
    valid_json: str,
):
    """
    Verify that an object instance is marshalled to JSON correctly.
    """
    # strictness=1 is used so that marshalling continues when
    # SchemaNotFound is raised
    marshalled = CODEC.dumps(instance, strictness=1)
    assert_json_is_equal(marshalled, valid_json)


def test_unmarshal(
    model_class: Type[CdmObject],
    valid_json: str,
    instance: CdmObject,
):
    """
    Verify that JSON is correctly unmarshalled to the expected instance.
    """
    # strictness=1 is used so that marshalling continues when
    # SchemaNotFound is raised
    unmarshalled = CODEC.loads(model_class, valid_json, strictness=1)
    assert unmarshalled == instance


def test_deserialising_invalid_json_raises_exception_when_strict(
    model_class: Type[CdmObject],
    invalid_json: str,
):
    """
    Verifies that unmarshaling an invalid JSON string results in an exception
    when the schema validation is set to strict.

    :param model_class: CdmObject class
    :param invalid_json: JSON string
    """
    with pytest.raises(JsonValidationError):
        CODEC.loads(model_class, invalid_json, strictness=2)


def test_serialising_valid_object_does_not_raise_exception_when_strict(
    instance: CdmObject,
):
    """
    Verifies that marshaling a valid instance does not result in a validation
    error when the schema exists and schema validation is set to strict.

    :param instance: valid object
    """
    try:
        CODEC.dumps(instance, strictness=2)
    except SchemaNotFound:
        pass


def test_serialising_invalid_object_raises_exception_when_strict(
    instance: CdmObject,
    modifier_fn: ModifierType,
):
    """
    Verify that serialising an invalid object results in a validation error
    when validation is set to strict.

    :param instance: valid CdmObject instance
    :param modifier_fn: function that makes the valid object invalid
    """

    obj = copy.deepcopy(instance)
    modifier_fn(obj)

    with pytest.raises(JsonValidationError):
        CODEC.dumps(obj, strictness=2)
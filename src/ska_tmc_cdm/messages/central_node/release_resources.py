"""
The release_resources module provides simple Python representations of the
structured request and response for a TMC CentralNode.ReleaseResources call.
"""
from typing import Optional

from pydantic import (
    AliasChoices,
    Field,
    StrictBool,
    field_serializer,
    field_validator,
    model_validator,
)
from typing_extensions import Any, Self

from ska_tmc_cdm.messages.base import CdmObject

from .common import DishAllocation

__all__ = ["ReleaseResourcesRequest"]

SCHEMA = "https://schema.skao.int/ska-tmc-releaseresources/2.1"


# NB: The amount of custom handling on this specific class
# feels unnecessary and excessive. Can we simplify this and settle
# on one name/format for dish/dish_allocation/receptor_ids
class ReleaseResourcesRequest(CdmObject):
    """
    ReleaseResourcesRequest is a Python representation of the structured
    request for a TMC CentralNode.ReleaseResources call.

    :param interface: url string to determine JsonSchema version, defaults to
        https://schema.skao.int/ska-tmc-releaseresources/2.1 if not set
    :param transaction_id: ID for tracking requests
    :param subarray_id: the numeric SubArray ID (1..16)
    :param release_all: True to release all sub-array resources, False to
    release just those resources specified as other arguments
    :param dish_allocation: object holding the DISH resource allocation
    to release for this request.
    """

    interface: Optional[str] = SCHEMA
    transaction_id: Optional[str] = None
    subarray_id: Optional[int] = None
    release_all: StrictBool = False
    dish: Optional[DishAllocation] = Field(
        default=None,
        serialization_alias="receptor_ids",
        validation_alias=AliasChoices(
            "receptor_ids", "dish_allocation", "dish"
        ),
    )

    # Custom logic required to mimic the behavior of marshallow.fields.Pluck()
    # to maintain backwards compatibility when removing Marshmallow schemas.
    # https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Pluck
    @field_serializer("dish", when_used="json-unless-none")
    def _flatten_to_receptor_ids(self, value: DishAllocation) -> list[str]:
        return value.receptor_ids

    @field_validator("dish", mode="before")
    @classmethod
    def _rehydrate_to_dish_allocation(
        cls, value: Any
    ) -> Optional[DishAllocation]:
        if isinstance(value, DishAllocation):
            return value
        elif value:
            return DishAllocation(receptor_ids=value)

    @model_validator(mode="after")
    def validate_release_all_ignores_dish_allocation(
        self,
    ) -> Self:
        if self.release_all is False and self.dish is None:
            raise ValueError(
                "Either release_all or dish_allocation must be defined"
            )
        # TODO: Can we get remove this awkward set-to-none behavior and raise
        # a validation error instead? Callers should be told when they're passing
        # bad inputs, not have their input silently ignored.
        if self.release_all and self.dish is not None:
            # We want to do self.dish = None but this would trigger
            # infinite recursion since we have validate_assignment=True
            # # and we're inside a validator:
            # https://github.com/pydantic/pydantic/issues/8185
            self.__dict__["dish"] = None
            # (pylint doesn't see __pydantic_fields_set__ as a set)
            # pylint: disable=no-member
            self.__pydantic_fields_set__.add("dish")
        return self

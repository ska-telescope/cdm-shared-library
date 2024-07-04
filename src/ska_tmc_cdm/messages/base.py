from os import environ
from typing import Union, cast, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    SerializerFunctionWrapHandler,
    model_serializer,
)
from pydantic.config import ExtraValues
from pydantic_core import PydanticUndefined

# Defaults to 'ignore' (silently accept), it can be helpful to set 'forbid'
# to catch errors during development:
EXTRA_FIELDS = cast(Union[ExtraValues, None], environ.get("EXTRA_FIELDS"))


class CdmObject(BaseModel):
    """Shared Base Class for all CDM Objects."""

    # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict
    model_config = ConfigDict(
        extra=EXTRA_FIELDS,
        # Serialize timedelta to floats of seconds:
        ser_json_timedelta="float",
        # Validate assignments and defaults to help keep ourselves honest:
        validate_assignment=True,
        validate_default=True,
    )

    def _is_default(self, key: str) -> bool:
        field_info = self.model_fields[key]
        if field_info.default_factory is not None:
            default = field_info.default_factory()
        elif field_info.default is not PydanticUndefined:
            default = field_info.default
        else:
            default = PydanticUndefined
        return getattr(self, key) == default

    @staticmethod
    def _is_empty(value: Any) -> bool:
        return value in (None, [], {})

    def _exclude_default_nulls_and_empty(
        self, dumped: dict[str, Any]
    ) -> dict[str, Any]:
        """To avoid cluttering JSON output, we want to omit any None, [], {} values
        that are present by default, but preserve any 'empty' values that were deliberately
        set by callers."""
        filtered = {
            key: val
            for key, val in dumped.items()
            if not (self._is_empty(val) and self._is_default(key))
        }
        return filtered

    @model_serializer(mode="wrap")
    def _serialize(
        self, default_serializer: SerializerFunctionWrapHandler
    ) -> dict[str, Any]:
        dumped = default_serializer(self)
        without_nulls = self._exclude_default_nulls_and_empty(dumped)
        return without_nulls

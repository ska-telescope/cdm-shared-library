from os import environ
from typing import Any, Tuple, Union, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    FieldSerializationInfo,
    SerializerFunctionWrapHandler,
    model_serializer,
)
from pydantic.config import ExtraValues
from pydantic.fields import FieldInfo
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

    @model_serializer(mode="wrap")
    def _serialize(
        self, default_serializer: SerializerFunctionWrapHandler
    ) -> dict[str, Any]:
        dumped = default_serializer(self)
        without_nulls = self._exclude_default_nulls_and_empty(dumped)
        return without_nulls

    def _exclude_default_nulls_and_empty(
        self, dumped: dict[str, Any]
    ) -> dict[str, Any]:
        """To avoid cluttering JSON output, we want to omit any None, [], {} values
        that are present by default, but preserve any 'empty' values that were deliberately
        set by callers or where the field is explicitly set exclude=False - requiring that it
        be included in serialised output."""
        filtered = {
            key: val
            for key, val in dumped.items()
            if self._must_include(key)
            or not (self._is_empty(val) and self._is_default(key))
        }
        return filtered

    def _get_field_info(self, key: str) -> Tuple[str, FieldInfo]:
        try:
            return key, self.model_fields[key]
        except KeyError:
            for name, info in self.model_fields.items():
                if key == info.serialization_alias:
                    return name, info
        raise ValueError(f"Unknown field name/alias: {key}")

    def _is_default(self, key: str) -> bool:
        field_name, field_info = self._get_field_info(key)
        if field_info.default_factory is not None:
            default = field_info.default_factory()
        elif field_info.default is not PydanticUndefined:
            default = field_info.default
        else:
            default = PydanticUndefined
        return getattr(self, field_name) == default

    def _must_include(self, key: str) -> bool:
        _, field_info = self._get_field_info(key)
        if field_info.exclude is False:
            return True
        else:
            return False

    @staticmethod
    def _is_empty(value: Any) -> bool:
        return value in (None, [], {})

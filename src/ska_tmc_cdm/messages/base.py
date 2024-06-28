from os import environ
from typing import Union, cast

from pydantic import BaseModel, ConfigDict
from pydantic.config import ExtraValues

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

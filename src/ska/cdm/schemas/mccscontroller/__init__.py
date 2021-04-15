"""
The schemas.mccscontroller package contains Marshmallow schemas that convert
JSON to/from the Python classes contained in ska.cdm.messages.mccscontroller.
"""
# runtime import required to register Marshmallow schema to the Python object
# model
from . import (   # noqa F401
    allocate,
    releaseresources
)

"""
The schemas.mccscontroller package contains Marshmallow schemas that convert
JSON to/from the Python classes contained in ska_tmc_cdm.messages.mccscontroller.
"""
# runtime import required to register Marshmallow schema to the Python object
# model
from . import allocate, releaseresources  # noqa F401

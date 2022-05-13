"""
The schemas.mccssubarray package contains Marshmallow schemas that convert
JSON to/from the Python classes contained in ska_tmc_cdm.messages.mccssubarray.
"""
# runtime import required to register Marshmallow schema to the Python object
# model
from . import assigned_resources, configure, scan  # noqa F401

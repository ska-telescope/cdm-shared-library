"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""

__all__ = [
    "ConfigureRequestSchema",
    "DishConfigurationSchema",
    "PointingSchema",
    "TargetSchema",
    "CSPConfigurationSchema",
    "SubarrayConfigurationSchema",
    "CommonConfigurationSchema",
    "CBFConfigurationSchema",
    "FSPConfigurationSchema",
    "SDPConfigurationSchema",
    "MCCSConfigurationSchema",
    "StnConfigurationSchema",
    "SubarrayBeamConfigurationSchema",
    "LowCBFConfigurationSchema",
]

from .core import (
    ConfigureRequestSchema,
    DishConfigurationSchema,
    PointingSchema,
    TargetSchema,
)
from .csp import (
    CBFConfigurationSchema,
    CommonConfigurationSchema,
    CSPConfigurationSchema,
    FSPConfigurationSchema,
    SubarrayConfigurationSchema,
)
from .mccs import (
    MCCSConfigurationSchema,
    StnConfigurationSchema,
    SubarrayBeamConfigurationSchema,
)
from .sdp import SDPConfigurationSchema

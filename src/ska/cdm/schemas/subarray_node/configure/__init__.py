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
    "StnBeamConfigurationSchema",
]

from .core import (
    ConfigureRequestSchema,
    DishConfigurationSchema,
    PointingSchema,
    TargetSchema,
)
from .csp import (
    CSPConfigurationSchema,
    FSPConfigurationSchema,
    SubarrayConfigurationSchema,
    CommonConfigurationSchema,
    CBFConfigurationSchema
)
from .sdp import SDPConfigurationSchema
from .mccs import (
    MCCSConfigurationSchema,
    StnConfigurationSchema,
    StnBeamConfigurationSchema,
)

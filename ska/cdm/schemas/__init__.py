"""
The  schemas for the SKA Configuration Data Model (CDM).
"""
__all__ = ['CODEC']

from .codec import MarshmallowCodec

CODEC = MarshmallowCodec()
# this is intentional because CODEC has to be defined before these are included
# pylint: disable=wrong-import-position
from . import central_node, subarray_node

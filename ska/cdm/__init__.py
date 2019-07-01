"""
The ska.cdm module contains data model and serialisation classes for the SKA
Configuration Data Model (CDM).
"""
from .schemas import MarshmallowCodec
from . import messages

__all__ = ['CODEC']

CODEC = MarshmallowCodec()

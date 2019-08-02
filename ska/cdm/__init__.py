"""
The ska.cdm module contains data model and serialisation classes for the SKA
Configuration Data Model (CDM).
"""
from . import messages
from .schemas.codec import CODEC

__all__ = ['CODEC']

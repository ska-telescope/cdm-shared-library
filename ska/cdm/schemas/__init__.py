__all__ = ['CODEC']

from .codec import MarshmallowCodec

CODEC = MarshmallowCodec()

from . import central_node, subarray_node

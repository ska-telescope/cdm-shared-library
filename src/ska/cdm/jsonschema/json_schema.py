"""
The JSON Schema module contains methods for fetching version-specific JSON schemas from the remote server.
It stores remote JSON schemas in the cache memory and uses it for marshmallow schema validation.
"""

import requests
import json
from functools import lru_cache, wraps
from datetime import datetime, timedelta

__all__ = ['JsonSchema']


def timed_lru_cache(seconds: int, maxsize: int = 128):
    """
     @timed_lru_cache decorator use to set the cache expiry on both time and space
    """
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


class JsonSchema:  # pylint: disable=too-few-public-methods
    """
    JSON Schema use for validating the structure of JSON data
    """

    def __init__(self):
        pass

    def get_schema_from_server(self, url: str):
        """
        Retrieve JSON Schemas from remote server.

        :param url: remote server url
        :return: JsonSchema
        """
        try:
            # print("fetching from server")
            response = requests.get(url)
            return json.loads(response.text)
        except Exception as err:
            return f'received exception {err}'

    @timed_lru_cache(3600)
    def get_json_schema(self, url: str):
        """
        Retrieve JSON Schemas from cache memory.Cache expiry is set to 3600 seconds.

        :param url: remote server url
        :return: JsonSchema
        """
        return self.get_schema_from_server(url)

    def validate_schema(self, schema, json):
        pass


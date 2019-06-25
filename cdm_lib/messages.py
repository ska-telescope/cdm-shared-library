"""Common Data Module (CDM) Library
Provides an implementaion of the JSON message between TMC and OET
"""
from cdm_lib.schemas import SubArray, SubArraySchema, Dish, cdm_to_obj, cdm_to_json

class AssignResources:
    """ Representation of the AssignResources request """
    _schema = SubArraySchema()

    def __init__(self, subarray_id: int, dish: Dish):
        self.subarray = SubArray(subarray_id, dish)

    def __repr__(self):
        return cdm_to_json(self._schema, self.subarray)

    @classmethod
    def from_request(cls, json_str):
        """Return an AssignResource object from a json string"""
        subarray = cdm_to_obj(cls._schema, json_str)
        return AssignResources(subarray.subarrayID, subarray.dish)

    @classmethod
    def from_subarray(cls, subarray):
        """Return an AssignResource object from a subarray object"""
        return AssignResources(subarray.subarrayID, subarray.dish)

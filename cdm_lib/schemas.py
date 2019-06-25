"""Common Data Module (CDM) Library
Provides an implementaion of the JSON message API between TMC and OET and
allows conversion between JSON messages and Python classes.
"""
from typing import Optional, List
from ast import literal_eval
from marshmallow import Schema, fields, post_load

class Dish:
    """ Represents an SKA Dish allocation - it contains the list of receptor IDs to be used"""

    def __init__(self, receptorIDList: Optional[List[str]] = None):
        if receptorIDList is None:
            self.receptorIDList = [] # pylint: disable=invalid-name
        self.receptorIDList = []
        for receptor_id in receptorIDList:
            self. receptorIDList.append(receptor_id)

    def __repr__(self):
        return format('<Dish( receptorIDList = {self.receptorIDList})>')


class SubArray:
    """ Represents a Subarray to be alocated. This consists of  id and a dish allocation
    element that holds the dish receptor IDs to be used """

    def __init__(self, subarrayID: int, dish: Dish):
        # As a user-facing class, handle both strings and ints
        self.dish = dish             # pylint: disable=invalid-name
        self.subarrayID = subarrayID # pylint: disable=invalid-name

    def __repr__(self):
        return format('<SubArray(subarrayID = {self.subarrayID}, dish = {self.dish})>')


class DishSchema(Schema):
    """ Schema used to convert betwen the Dish object and its JSON representation """

    # dish consists of a list of receptorIds
    receptorIDList = fields.List(fields.Str())

    # this annotation defines any operations needed after load.
    # If we needed to do any work on the object we could do it here
    # in this case we are just treating each of the named arguments
    # we were passed to the equivalent named argument and letting
    # the __init__ do the work.
    @post_load
    def create_dish(self, data, **kwargs): # pylint: disable=no-self-use
        """ handle any internal logic needed - at the moment this is purely static
        as all it does is return the dish"""
        return Dish(**data)


class SubArraySchema(Schema):
    """ Schema used to convert betwen the Schema object and its JSON representation """
    subarrayID = fields.Integer()

    # contains a nested 'dish'
    dish = fields.Nested(DishSchema)
    class Meta:
        fields = ("subarrayID", "dish")
        ordered = True


    @post_load
    def create_subarray(self, data, **kwargs):
        """ this method hdles  any operations needed after the JSON is loaded """
        return SubArray(**data)


def cdm_to_json(schema, obj):
    """ convert the object into a json string. """
    #We could use schema.dump
    # if we only needed it as a dictionary representation
    result = schema.dumps(obj)
    return result


def cdm_to_obj(schema, json_str):
    """ convert to a python object"""
    # assuming we get a string as input so eval to create the initial
    # dictionary representation
    json_dict = literal_eval(json_str)
    result = schema.load(json_dict)
    return result

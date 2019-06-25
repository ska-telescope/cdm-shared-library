"""Example of using the cdm_lib methods directly based on the AssignResources request """

from cdm_lib.schemas import Dish, SubArray, SubArraySchema, cdm_to_json, cdm_to_obj

def assign_resources_example():
    """
    Example of creating an AssignResources showing how the cdm methods can be used to
    create a JSON request
    """

    example_json = """{
    "subarrayID": 1, 
        "dish": {
            "receptorIDList": ["0001", "0002"]
        }
    }"""

    # Instance of the schema that we are going to use to do the work
    schema = SubArraySchema()

    # create a python object
    dish = Dish(receptorIDList=["00001", "00002"])
    sub_array = SubArray(1, dish)

    # convert to json
    sub_json = cdm_to_json(schema, sub_array)
    print(sub_json)

    # convert the example json string to a python object
    sub_obj = cdm_to_obj(schema, example_json)
    print(sub_obj)

if __name__ == '__main__':
    assign_resources_example()

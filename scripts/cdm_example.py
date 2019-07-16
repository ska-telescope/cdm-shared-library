 """Example of using the cdm methods directly based on the AssignResourcesRequest request """

from ska.cdm import CODEC
import ska.cdm.messages.central_node as cn

if __name__ == '__main__':
    allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    request = cn.AssignResourcesRequest(1, dish_allocation=allocation)

    json_str = CODEC.dumps(request)
    assert (json_str == '{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}')

    obj = CODEC.loads(cn.AssignResourcesRequest, json_str)

    assert obj == request

"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_dump, post_load

import ska.cdm.messages.central_node.assign_resources as assign_msgs
import ska.cdm.messages.central_node.release_resources as release_msgs
from . import CODEC

__all__ = ['AssignResourcesRequestSchema',
           'AssignResourcesResponseSchema',
           'DishAllocationSchema',
           'DishAllocationResponseSchema',
           'ReleaseResourcesRequestSchema']


class DishAllocationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the DishAllocation class.
    """

    receptor_ids = fields.List(fields.String, data_key='receptorIDList', many=True, required=True)

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a DishAllocation object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: DishAllocation object populated from data
        """
        receptor_ids = data['receptor_ids']
        return assign_msgs.DishAllocation(receptor_ids=receptor_ids)


@CODEC.register_mapping(assign_msgs.DishAllocation)
class DishAllocationResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the DishAllocation class when received in the
    response.
    """
    receptor_ids = fields.List(fields.String, data_key='receptorIDList_success', many=True,
                               required=True)

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON from an AssignResources response back into a
        DishAllocation object.

        This 'duplicate' schema is required as the DishAllocation is found
        under a different JSON key in the response as compared to the request.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: DishAllocation object populated from data
        """
        receptor_ids = data['receptor_ids']
        return assign_msgs.DishAllocation(receptor_ids=receptor_ids)


@CODEC.register_mapping(assign_msgs.AssignResourcesRequest)
class AssignResourcesRequestSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the AssignResourcesRequest class.
    """

    subarray_id = fields.Integer(data_key='subarrayID', required=True)
    dish = fields.Nested(DishAllocationSchema, data_key='dish', required=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        marshmallow directives for AssignResourcesRequestSchema.
        """
        ordered = True

    @post_load
    def create_request(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into an AssignResources request object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: AssignResources object populated from data
        """
        subarray_id = data['subarray_id']
        dish_allocation = data['dish']
        return assign_msgs.AssignResourcesRequest(subarray_id, dish_allocation=dish_allocation)


@CODEC.register_mapping(assign_msgs.AssignResourcesResponse)
class AssignResourcesResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the AssignResourcesResponse class.
    """

    dish = fields.Nested(DishAllocationResponseSchema, data_key='dish', required=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Marshmallow directives for AssignResourcesResponseSchema.
        """
        ordered = True

    @post_load
    def create_response(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON from an AssignResources response back into an
        AssignResourcesResponse object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: AssignResourcesResponse object populated from data
        """
        dish_allocation = data['dish']
        return assign_msgs.AssignResourcesResponse(dish_allocation=dish_allocation)


@CODEC.register_mapping(release_msgs.ReleaseResourcesRequest)
class ReleaseResourcesRequestSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the ReleaseResourcesRequest class.
    """

    subarray_id = fields.Integer(data_key='subarrayID', required=True)
    dish = fields.Nested(DishAllocationSchema, data_key='dish')
    release_all = fields.Boolean(data_key='releaseALL')

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Marshmallow directives for ReleaseResourcesRequestSchema.
        """
        ordered = True

    @post_dump
    def filter_args(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter Marshmallow's JSON based on the value of release_all.

        If release_all is True, other resource definitions should be stripped
        from the request. If release_all if False, the 'release_all' key
        itself should be stripped.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for request submission
        """
        # If release_all is True, other resources should be stripped - and
        # vice versa
        release_all = data['releaseALL']
        if release_all:
            del data['dish']
        else:
            del data['releaseALL']
        return data

    @post_load
    def create_request(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON from an ReleaseResources request back into an
        ReleaseResourcesRequest object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ReleaseResourcesRequest object populated from data
        """
        subarray_id = data['subarray_id']
        release_all = data.get('release_all', False)
        dish_allocation = data.get('dish', None)
        return release_msgs.ReleaseResourcesRequest(subarray_id, release_all=release_all,
                                                    dish_allocation=dish_allocation)

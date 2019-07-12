"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_load, post_dump, pre_dump
from astropy.coordinates import SkyCoord

from .messages.central_node import AssignResourcesRequest, AssignResourcesResponse, \
    DishAllocation, ReleaseResourcesRequest
from .messages.subarray_node import ConfigureRequest, DishConfiguration, PointingConfiguration

__all__ = ['AssignResourcesRequestSchema', 'AssignResourcesResponseSchema', 'DishAllocationSchema',
           'ReleaseResourcesRequestSchema', 'MarshmallowCodec']


class DishAllocationSchema(Schema):
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
        return DishAllocation(receptor_ids=receptor_ids)


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
        return AssignResourcesRequest(subarray_id, dish_allocation=dish_allocation)


class DishAllocationResponseSchema(Schema):
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
        return DishAllocation(receptor_ids=receptor_ids)


class AssignResourcesResponseSchema(Schema):
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
        return AssignResourcesResponse(dish_allocation=dish_allocation)


class ReleaseResourcesRequestSchema(Schema):
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
        :return: ReleasResourcesRequest object populated from data
        """
        subarray_id = data['subarray_id']
        release_all = data.get('release_all', False)
        dish_allocation = data.get('dish', None)
        return ReleaseResourcesRequest(subarray_id, release_all=release_all,
                                       dish_allocation=dish_allocation)

class SkyCoordSchema(Schema):
    ra = fields.Float(attribute='ra.rad')
    dec = fields.Float(attribute='dec.rad')
    frame = fields.String(attribute='frame.name')
    name = fields.String(attribute='info.name')

    @pre_dump
    def convert_to_icrs(self, data, **_):
        converted = data.transform_to('icrs')
        converted.info.name = data.info.name
        return converted

    @post_load
    def create_skycoord(self, data):
        ra = data['ra']
        dec = data['dec']
        frame = data['frame']
        name = data['name']
        sky_coord = SkyCoord(ra=ra, dec=dec, frame=frame)
        sky_coord.info.name = name
        return sky_coord


class PointingSchema(Schema):
    target = fields.Nested(SkyCoordSchema)

    @post_load
    def create(self, data, **_):
        target = data['target']
        return PointingConfiguration(target)


class DishConfigurationSchema(Schema):
    receiver_band = fields.String(data_key='receiverBand', required=True)

    @post_load
    def create_dish_configuration(self, data, **_):
        receiver_band = data['receiver_band']
        return DishConfiguration(receiver_band)


class ConfigureRequestSchema(Schema):
    pointing = fields.Nested(PointingSchema)
    dish = fields.Nested(DishConfigurationSchema)

    @post_load
    def create_configuration(self, data, **_):
        pointing = data['pointing']
        dish_configuration = data['dish']
        return ConfigureRequest(pointing, dish_configuration)

class MarshmallowCodec:
    """
    MarshmallowCodec marshalls and unmarshalls CDM classes.

    The mapping of CDM classes to Marshmallow schema is defined in this class.
    """

    def __init__(self):
        self.schema = {
            AssignResourcesRequest: AssignResourcesRequestSchema,
            AssignResourcesResponse: AssignResourcesResponseSchema,
            ReleaseResourcesRequest: ReleaseResourcesRequestSchema,
            DishAllocation: DishAllocationSchema
        }

    def load_from_file(self, cls, path):
        """
        Load an instance of a CDM class from disk.

        :param cls: the class to create from the file
        :param path: the path to the file
        :return: an instance of cls
        """
        with open(path, 'r') as json_file:
            json_data = json_file.read()
            return self.loads(cls, json_data)

    def loads(self, cls, json_data):
        """
        Create an instance of a CDM class from a JSON string.

        :param cls: the class to create from the JSON
        :param json_data: the JSON to unmarshall
        :return: an instance of cls
        """
        schema_cls = self.schema[cls]
        schema_obj = schema_cls()
        return schema_obj.loads(json_data=json_data)

    def dumps(self, obj):
        """
        Return a string JSON representation of a class.

        :param obj: the instance to marshall to JSON
        :return: a JSON string
        """
        schema_cls = self.schema[obj.__class__]
        schema_obj = schema_cls()
        return schema_obj.dumps(obj)

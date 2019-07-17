"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""
from datetime import timedelta

from marshmallow import Schema, fields, post_load, post_dump, pre_dump
from marshmallow.validate import OneOf

from .messages import central_node as cn
from .messages import subarray_node as sn

__all__ = ['AssignResourcesRequestSchema', 'AssignResourcesResponseSchema', 'DishAllocationSchema',
           'ReleaseResourcesRequestSchema', 'ConfigureRequestSchema', 'ScanRequestSchema', 'MarshmallowCodec']


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
        return cn.DishAllocation(receptor_ids=receptor_ids)


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
        return cn.AssignResourcesRequest(subarray_id, dish_allocation=dish_allocation)


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
        return cn.DishAllocation(receptor_ids=receptor_ids)


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
        return cn.AssignResourcesResponse(dish_allocation=dish_allocation)


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
        :return: ReleaseResourcesRequest object populated from data
        """
        subarray_id = data['subarray_id']
        release_all = data.get('release_all', False)
        dish_allocation = data.get('dish', None)
        return cn.ReleaseResourcesRequest(subarray_id, release_all=release_all,
                                          dish_allocation=dish_allocation)


class UpperCasedField(fields.Field):
    """
    Field that serializes to an upper-case string and deserializes
    to a lower-case string.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return value.upper()

    def _deserialize(self, value, attr, data, **kwargs):
        return value.lower()


class TargetSchema(Schema):
    """
    Marshmallow schema for the subarray_node.Target class
    """

    ra = fields.Float(attribute='coord.ra.rad', data_key='RA')
    dec = fields.Float(attribute='coord.dec.rad')
    frame = UpperCasedField(attribute='coord.frame.name', data_key='system')
    name = fields.String()

    @pre_dump
    def convert_to_icrs(self, target: sn.Target, **_):  # pylint: disable=no-self-use
        """
        Process Target co-ordinates by converting them to ICRS frame before
        the JSON marshalling process begins.

        :param target: Target instance to process
        :param _: kwargs passed by Marshallow
        :return: Target with co-ordinates expressed in ICRS.
        """
        # All pointing coordinates are in ICRS
        target.coord = target.coord.transform_to('icrs')
        return target

    @post_load
    def create_target(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Target object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: Target instance populated to match JSON
        """
        name = data['name']
        coord = data['coord']
        ra_rad = coord['ra']['rad']
        dec_rad = coord['dec']['rad']
        frame = coord['frame']['name']
        target = sn.Target(ra_rad, dec_rad, frame=frame, name=name, unit='rad')
        return target


class PointingSchema(Schema):
    """
    Marshmallow schema for the subarray_node.Pointing class.
    """

    target = fields.Nested(TargetSchema)

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a subarray_node.Pointing object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: Pointing instance populated to match JSON
        """
        target = data['target']
        return sn.PointingConfiguration(target)


class DishConfigurationSchema(Schema):
    """
    Marshmallow schema for the subarray_node.DishConfiguration class.
    """

    receiver_band = fields.String(data_key='receiverBand', required=True,
                                  validate=OneOf(['1', '2', '5a', '5b']))

    @pre_dump
    def convert(self, dish_configuration: sn.DishConfiguration, **_):  # pylint: disable=no-self-use
        """
        Process DishConfiguration instance so that it is ready for conversion
        to JSON.

        :param dish_configuration:
        :param _: kwargs passed by Marshmallow
        :return: DishConfiguration instance populated to match JSON
        """
        # Convert Python Enum to its string value
        dish_configuration.receiver_band = dish_configuration.receiver_band.value
        return dish_configuration

    @post_load
    def create_dish_configuration(self, data, **_):  # pylint: disable=no-self-use
        """
        Converted parsed JSON back into a subarray_node.DishConfiguration
        object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: DishConfiguration instance populated to match JSON
        """
        receiver_band = data['receiver_band']
        enum_obj = sn.ReceiverBand(receiver_band)
        return sn.DishConfiguration(enum_obj)


class ConfigureRequestSchema(Schema):
    """
    Marshmallow schema for the subarray_node.ConfigureRequest class.
    """

    pointing = fields.Nested(PointingSchema)
    dish = fields.Nested(DishConfigurationSchema)

    @post_load
    def create_configuration(self, data, **_):  # pylint: disable=no-self-use
        """
        Converted parsed JSON backn into a subarray_node.ConfigureRequest
        object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ConfigurationRequest instance populated to match JSON
        """
        pointing = data['pointing']
        dish_configuration = data['dish']
        return sn.ConfigureRequest(pointing, dish_configuration)



class ScanRequestSchema(Schema):
    """
    Create the Schema for ScanDuration using timedelta
    """
    scan_duration = fields.Float()

    @pre_dump
    def convert_to_scan(self, data, **_):
        duration = data.scan_duration
        in_secs = duration.total_seconds()
        data.scan_duration = in_secs
        return data

    @post_load
    def create_scan_request(self, data, **_):
        t = timedelta(seconds=data['scan_duration'])
        scan_request = sn.ScanRequest(t)
        return scan_request


class MarshmallowCodec:
    """
    MarshmallowCodec marshalls and unmarshalls CDM classes.

    The mapping of CDM classes to Marshmallow schema is defined in this class.
    """

    def __init__(self):
        self.schema = {
            cn.AssignResourcesRequest: AssignResourcesRequestSchema,
            cn.AssignResourcesResponse: AssignResourcesResponseSchema,
            cn.ReleaseResourcesRequest: ReleaseResourcesRequestSchema,
            cn.DishAllocation: DishAllocationSchema,
            sn.ConfigureRequest: ConfigureRequestSchema
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

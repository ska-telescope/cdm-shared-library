"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""
import collections
from datetime import timedelta

from marshmallow import Schema, fields, post_load, post_dump, pre_dump
from marshmallow.validate import OneOf

from .messages import central_node as cn
from .messages import subarray_node as sn

__all__ = ['AssignResourcesRequestSchema', 'AssignResourcesResponseSchema', 'DishAllocationSchema',
           'ReleaseResourcesRequestSchema', 'ConfigureRequestSchema', 'ScanRequestSchema',
           'MarshmallowCodec',
           'SDPConfigurationBlockSchema', 'SDPConfigureSchema', 'SDPConfigureScanSchema', 'SDPParametersSchema',
           'SDPScanSchema',
           'SDPScanParametersSchema']


class OrderedSchema(Schema):
    class Meta:  # pylint: disable=too-few-public-methods
        """
        marshmallow directive to respect order of JSON properties  in message.
        """
        ordered = True


SexagesimalTarget = collections.namedtuple('SexagesimalTarget', 'ra dec frame name')


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


class TargetSchema(OrderedSchema):
    """
    Marshmallow schema for the subarray_node.Target class
    """

    ra = fields.String(data_key='RA')
    dec = fields.String()
    frame = UpperCasedField(data_key='system')
    name = fields.String()

    @pre_dump
    def convert_to_icrs(self, target: sn.Target, **_):  # pylint: disable=no-self-use
        """
        Process Target co-ordinates by converting them to ICRS frame before
        the JSON marshalling process begins.

        :param target: Target instance to process
        :param _: kwargs passed by Marshallow
        :return: SexagesimalTarget with ICRS ra/dec expressed in hms/dms
        """
        # All pointing coordinates are in ICRS
        icrs_coord = target.coord.transform_to('icrs')
        hms, dms = icrs_coord.to_string('hmsdms', sep=':').split(' ')
        sexagesimal = SexagesimalTarget(
            ra=hms, dec=dms, frame=icrs_coord.frame.name, name=target.name
        )

        return sexagesimal

    @post_load
    def create_target(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Target object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: Target instance populated to match JSON
        """
        name = data['name']
        hms = data['ra']
        dms = data['dec']
        frame = data['frame']
        target = sn.Target(hms, dms, frame=frame, name=name, unit=('hourangle', 'deg'))
        return target


# Added for clarity that SDP is currently assumed to require RA and Dec as radians
# unlike the TMC need for a sexagesimal target
RadianTarget = collections.namedtuple('RadianTarget', 'ra dec frame name')


class SDPTargetSchema(OrderedSchema):
    """
    Marshmallow schema for the subarray_node.Target class when used for the 
    SDP Target. This is similar to the Pointing Target but uses lower case for the
    name for the ra parameter and seems to assume radians rather than sexagesimal 
    format for RA and Dec - if these differences are resolved this schema will become
    redundant.
    """
    frame = UpperCasedField(data_key='system')
    name = fields.String()
    ra = fields.Float(data_key='ra')
    dec = fields.Float()

    @pre_dump
    def convert_to_icrs(self, target: sn.Target, **_):  # pylint: disable=no-self-use
        """
        Process Target co-ordinates by converting them to ICRS frame before
        the JSON marshalling process begins.

        :param target: Target instance to process
        :param _: kwargs passed by Marshmallow
        :return: Basic target with ra/dec expressed in radians
        """
        # All pointing coordinates are in ICRS
        target.coord = target.coord.transform_to('icrs')
        ra = target.coord.ra.rad
        dec = target.coord.dec.rad
        target_radians = RadianTarget(
            frame=target.coord.frame.name, name=target.name, ra=ra, dec=dec
        )
        return target_radians

    @post_load
    def create_target(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Target object. We are assuming that on the
        SDPRequest the target is expressed in radians.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: Target instance populated to match JSON
        """
        name = data['name']
        ra_rad = data['ra']['rad']
        dec_rad = data['dec']['rad']
        frame = data['frame']
        target = sn.Target(ra=ra_rad, dec=dec_rad, frame=frame, name=name, unit='rad')
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

    scan_id = fields.Integer(required=True, data_key='scanID')
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
        scan_id = data['scan_id']
        pointing = data['pointing']
        dish_configuration = data['dish']
        return sn.ConfigureRequest(scan_id, pointing, dish_configuration)


class ScanRequestSchema(Schema):
    """
    Create the Schema for ScanDuration using timedelta
    """
    scan_duration = fields.Float()

    @pre_dump
    def convert_to_scan(self, data, **_):  # pylint: disable=no-self-use
        """
        Process scan_duration and converted it
        in a float using total_seconds method
        :param data: the scan_duration timedelta
        :param _: kwargs passed by Marshallow
        :return: float converted
        """
        duration = data.scan_duration
        in_secs = duration.total_seconds()
        data.scan_duration = in_secs
        return data

    @post_load
    def create_scan_request(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanRequest
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanRequest instance populated to match JSON
        """
        t_to_scan = timedelta(seconds=data['scan_duration'])
        scan_request = sn.ScanRequest(t_to_scan)
        return scan_request


class SDPWorkflowSchema(OrderedSchema):
    wf_id = fields.String(data_key='id', required=True)
    wf_type = fields.String(data_key='type', required=True)
    version = fields.String(data_key='version', required=True)
    sdp_workflow = sn.SDPWorkflow


class SDPParametersSchema(OrderedSchema):
    num_stations = fields.Int(data_key='numStations', required=True)
    num_chanels = fields.Int(data_key='numChanels', required=True)
    num_polarisations = fields.Int(data_key='numPolarisations', required=True)
    freq_start_hz = fields.Float(data_key='freqStartHz', required=True)
    freq_end_hz = fields.Float(data_key='freqEndHz', required=True)
    target_fields = fields.Dict(data_key='fields', keys=fields.String(), values=fields.Nested(SDPTargetSchema),
                                required=True)


class SDPScanSchema(OrderedSchema):
    field_id = fields.Int(data_key='fieldId', required=True)
    interval_ms = fields.Int(data_key='intervalMs', required=True)

    @post_load
    def create_sdp_scan(self, data, **_):  # pylint: disable=no-self-use
        field_id = data['fieldId']
        interval_ms = data['intervalMs']
        return sn.SDPScan(field_id, interval_ms)


class SDPScanParametersSchema(OrderedSchema):
    scan_parameters = fields.Dict(data_key='scanParameters', keys=fields.String(), values=fields.Nested(SDPScanSchema))


class SDPConfigureScanSchema(OrderedSchema):
    configure_scan = fields.Nested(SDPScanParametersSchema, data_key="configureScan", required=True)

    @post_load
    def create_sdp_configure_scan(self, data, **_):  # pylint: disable=no-self-use
        configure_scan = data['configureScan']
        return sn.SDPConfigureScan(configure_scan=configure_scan)


class SDPConfigurationBlockSchema(OrderedSchema):
    sb_id = fields.String(data_key='id', required=True)
    sbi_id = fields.String(data_key='sbiId', required=True)
    workflow = fields.Nested(SDPWorkflowSchema)
    parameters = fields.Nested(SDPParametersSchema)
    scan_parameters = fields.Dict(data_key='scanParameters', keys=fields.String(), values=fields.Nested(SDPScanSchema))

    @post_load
    def create_sdp_configure_block(self, data, **_):  # pylint: disable=no-self-use
        sb_id = data['id']
        sbi_id = data['sbi_id]']
        workflow = data['workflow']
        parameters = data['parameters']
        scan_parameters = data['scanParameters']
        return sn.SDPConfigurationBlock(sb_id=sb_id, sbi_id=sbi_id, workflow=workflow,
                                        parameters=parameters, scan_parameters=scan_parameters)


class SDPConfigureSchema(OrderedSchema):
    configure = fields.List(fields.Nested(SDPConfigurationBlockSchema, required=True))

    @post_load
    def create_sdp_configure(self, data, **_):  # pylint: disable=no-self-use
        configure = data['configure']
        return sn.SDPConfigure(configure)


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
            sn.ConfigureRequest: ConfigureRequestSchema,
            sn.ScanRequest: ScanRequestSchema,
            sn.SDPConfigurationBlock: SDPConfigurationBlockSchema,
            sn.SDPConfigure: SDPConfigureSchema,
            sn.SDPConfigureScan: SDPConfigureScanSchema
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

"""
This module defines Marshmallow schemas that map CDM the message classes for
SDP configuration to and from a JSON representation.
"""
import collections

from marshmallow import Schema, fields, post_dump, post_load, pre_dump

import ska.cdm.messages.subarray_node.configure as configure_msgs
from ... import shared

__all__ = ['ProcessingBlockConfigurationSchema',
           'SDPConfigurationSchema',
           'SDPParametersSchema',
           'SDPScanParametersSchema',
           'SDPScanSchema',
           'SDPTargetSchema',
           'SDPWorkflowSchema']

JsonTarget = collections.namedtuple('JsonTarget', 'ra dec frame name')


class SDPTargetSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the subarray_node.Target class when used for the
    SDP Target. This is similar to the Pointing Target but uses lower case for the
    name for the ra parameter and seems to assume radians rather than sexagesimal
    format for RA and Dec - if these differences are resolved this schema will become
    redundant.
    """
    frame = shared.UpperCasedField(data_key='system')
    name = fields.String()
    ra = fields.Float(data_key='ra')
    dec = fields.Float()

    @pre_dump
    def convert_to_icrs(self, target: configure_msgs.Target, **_):  # pylint: disable=no-self-use
        """
        Process Target co-ordinates by converting them to ICRS frame before
        the JSON marshalling process begins.

        :param target: Target instance to process
        :param _: kwargs passed by Marshmallow
        :return: Basic target with ra/dec expressed in radians
        """
        # All pointing coordinates are in ICRS
        target.coord = target.coord.transform_to('icrs')
        ra_rad = target.coord.ra.rad
        dec_rad = target.coord.dec.rad
        target_radians = JsonTarget(
            frame=target.coord.frame.name, name=target.name, ra=ra_rad, dec=dec_rad
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
        ra_rad = data['ra']
        dec_rad = data['dec']
        frame = data['frame']
        target = configure_msgs.Target(ra=ra_rad, dec=dec_rad, frame=frame, name=name, unit='rad')
        return target


class SDPWorkflowSchema(Schema):  # pylint: disable=too-few-public-methods
    """Represents the type of workflow being configured on the SDP eventually this will tie
       into some kind of lookup/enumeration
    """
    workflow_id = fields.String(data_key='id', required=True)
    workflow_type = fields.String(data_key='type', required=True)
    version = fields.String(data_key='version', required=True)
    sdp_workflow = configure_msgs.SDPWorkflow

    @post_load
    def create_sdp_workflow(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Workflow definition (SDPWorkflow)
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPWorkflow instance populated to match JSON
        """
        wf_id = data['workflow_id']
        wf_type = data['workflow_type']
        version = data['version']
        return configure_msgs.SDPWorkflow(wf_id, wf_type, version)


class SDPParametersSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Represents the main SDP configuration parameters
    """
    num_stations = fields.Int(data_key='numStations')
    num_channels = fields.Int(data_key='numChannels')
    num_polarisations = fields.Int(data_key='numPolarisations')
    freq_start_hz = fields.Float(data_key='freqStartHz')
    freq_end_hz = fields.Float(data_key='freqEndHz')
    target_fields = fields.Dict(data_key='fields', keys=fields.String(),
                                values=fields.Nested(SDPTargetSchema))

    @post_load
    def create_sdp_parameters(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a set of SDP Parameters
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPParameters instance populated to match JSON
        """
        num_stations = data['num_stations']
        num_channels = data['num_channels']
        num_polarisations = data['num_polarisations']
        freq_start_hz = data['freq_start_hz']
        freq_end_hz = data['freq_end_hz']
        target_fields = data['target_fields']
        return configure_msgs.SDPParameters(num_stations, num_channels, num_polarisations,
                                            freq_start_hz, freq_end_hz, target_fields)


class SDPScanSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    The field id should match one of the previously defined fields in the targets dictionary.
    The interval is the integer number of millisecs for the scan.
    """
    field_id = fields.Int(data_key='fieldId', required=True)
    interval_ms = fields.Int(data_key='intervalMs', required=True)

    @post_load
    def create_sdp_scan(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a set of SDP Parameters
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPScan instance populated to match JSON
        """
        field_id = data['field_id']
        interval_ms = data['interval_ms']
        return configure_msgs.SDPScan(field_id, interval_ms)


class SDPScanParametersSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Scans are indexed by ScanID. It is not yet clear if we expect to send multiple scans within the
    same configuration - all the examples so far are for a single scan.
    For each subsiquet request we pass just the scan parameters.
    """
    scan_parameters = fields.Dict(data_key='scanParameters', keys=fields.String(),
                                  values=fields.Nested(SDPScanSchema))

    @post_load
    def create_sdp_scan_parameters(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a set containing all the scans
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPScanParameters instance populated to match JSON
        """
        scan_parameters = data['scan_parameters']
        return configure_msgs.SDPScanParameters(scan_parameters)


class ProcessingBlockConfigurationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow class for the ProcessingBlockConfiguration class
    On the initial configure scan a list of these blocks are provided to configure SDP
    """
    sb_id = fields.String(data_key='id', required=True)
    sbi_id = fields.String(data_key='sbiId', required=True)
    workflow = fields.Nested(SDPWorkflowSchema)
    parameters = fields.Nested(SDPParametersSchema)
    scan_parameters = fields.Dict(data_key='scanParameters', keys=fields.String(),
                                  values=fields.Nested(SDPScanSchema))

    @post_load
    def unmarshall(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a set containing all the scans
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ProcessingBlockConfiguration instance populated to match JSON
        """
        return configure_msgs.ProcessingBlockConfiguration(**data)


class SDPConfigurationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow class for the SDPConfigure class
    This is the top level schema for the SDP part of the configure scan request.
    It is going to consist of either a 'configure' request (first scan) or a
    'configureScan' (each subsequent request)
    """
    configure = fields.Nested(ProcessingBlockConfigurationSchema, many=True)
    configure_scan = fields.Nested(SDPScanParametersSchema, data_key='configureScan')

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SDP configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_sdp_configuration(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a set containing all the scans
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfigureScan instance populated to match JSON
        """
        return configure_msgs.SDPConfiguration(**data)


class NewSubBandSchema(Schema):
    """
    Represents ...
    """
    freq_min = fields.Float(data_key='freq_min', required=True) 
    freq_max = fields.Float(data_key='freq_max', required=True) 
    nchan = fields.Int(data_key='nchan', required=True)
    input_link_map = fields.List(fields.List(fields.Int), data_key='input_link_map', required=True)

    @post_load
    def create_sub_band(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a SubBand object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SubBand object populated from data
        """
        freq_min = data['freq_min']
        freq_max = data['freq_max']
        nchan = data['nchan']
        input_link_map = data['input_link_map']
        return configure_msgs.SubBand(freq_min, freq_max, nchan, input_link_map)


class NewScanTypeSchema(Schema):
    """
    Represents ...
    """
    st_id = fields.String(data_key='id', required=True)
    coordinate_system = fields.String(data_key='coordinate_system', required=True)
    ra = fields.String(data_key='ra', required=True)
    dec = fields.String(data_key='dec', required=True)
    sub_bands = fields.Nested(NewSubBandSchema, data_key='subbands', many=True)

    @post_load
    def create_scan_type(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanType object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanTypew object populated from data
        """
        st_id = data['st_id']
        coordinate_system = data['coordinate_system']
        ra = data['ra']
        dec = data['dec']
        sub_bands = data['sub_bands']
        return configure_msgs.ScanType(st_id, coordinate_system, ra, dec, sub_bands)


class NewSDPParametersSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Represents the main SDP configuration parameters
    """

    @post_load
    def create_sdp_parameters(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a SDPParameters object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPParameter object populated from data
        """
        # import pdb; pdb.set_trace()
        return configure_msgs.NewSDPParameters()


class NewSDPWorkflowSchema(Schema):  # pylint: disable=too-few-public-methods
    """Represents the type of workflow being configured on the SDP eventually this will tie
       into some kind of lookup/enumeration
    """
    workflow_id = fields.String(data_key='id', required=True)
    workflow_type = fields.String(data_key='type', required=True)
    version = fields.String(data_key='version', required=True)

    @post_load
    def create_sdp_wf(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a SDP Workflow object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDP Workflow object populated from data
        """
        wf_id = data['workflow_id']
        wf_type = data['workflow_type']
        version = data['version']
        return configure_msgs.SDPWorkflow(wf_id, wf_type, version)


class NewDependencySchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Represents ...
    """
    pb_id = fields.String(data_key='pb_id')
    pb_type = fields.List(fields.String, data_key='type')

    @post_load
    def create_pb_dependency(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a PbDependency object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: PbDependency object populated from data
        """
        pb_id = data['pb_id']
        pb_type = data['pb_type']
        return configure_msgs.PbDependency(pb_id, pb_type)


class NewProcessingBlockSchema(Schema):
    """
    Represents ...
    """
    pb_id = fields.String(data_key='id', required=True)
    workflow = fields.Nested(NewSDPWorkflowSchema)
    parameters = fields.Nested(NewSDPParametersSchema)
    dependencies = fields.Nested(NewDependencySchema, many=True, missing=None)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_processing_block_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a PB object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: PB object populated from data
        """
        return configure_msgs.NewProcessingBlockConfiguration(**data)


class NewSdpConfigurationSchema(Schema):
    """
    Marsmallow class for the NewSDPConfiguration class
    """
    sdp_id = fields.String(data_key='id', required=True)
    max_length = fields.Float(data_key="max_length", required=True)
    scan_types = fields.Nested(NewScanTypeSchema, many=True)
    processing_blocks = fields.Nested(NewProcessingBlockSchema, many=True)

    @post_load
    def create_sdp_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a NewSDPConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: NewSDPConfiguration object populated from data
        """
        return configure_msgs.NewSDPConfiguration(**data)

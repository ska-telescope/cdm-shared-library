"""
This module defines Marshmallow schemas that map CDM the message classes for
SDP configuration to and from a JSON representation.
"""
import collections

from marshmallow import Schema, fields, post_load, post_dump, pre_dump

from ska.cdm.messages import subarray_node as sn
from ska.cdm.schemas import shared

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
        target = sn.Target(ra=ra_rad, dec=dec_rad, frame=frame, name=name, unit='rad')
        return target


class SDPWorkflowSchema(Schema):  # pylint: disable=too-few-public-methods
    """Represents the type of workflow being configured on the SDP eventually this will tie
       into some kind of lookup/enumeration
    """
    id = fields.String(data_key='id', required=True)
    type = fields.String(data_key='type', required=True)
    version = fields.String(data_key='version', required=True)
    sdp_workflow = sn.SDPWorkflow

    @post_load
    def create_sdp_workflow(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Workflow definition (SDPWorkflow)
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPWorkflow instance populated to match JSON
        """
        wf_id = data['id']
        wf_type = data['type']
        version = data['version']
        return sn.SDPWorkflow(wf_id, wf_type, version)


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
        return sn.SDPParameters(num_stations, num_channels, num_polarisations,
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
        return sn.SDPScan(field_id, interval_ms)


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
        return sn.SDPScanParameters(scan_parameters)


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
        return sn.ProcessingBlockConfiguration(**data)


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
        return sn.SDPConfiguration(**data)

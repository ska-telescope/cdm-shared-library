"""
This module defines Marshmallow schemas that map the CDM classes for
SubArrayNode CSP configuration to/from JSON.
"""
from marshmallow import Schema, fields, post_load, pre_dump, post_dump
from marshmallow.validate import OneOf

import ska.cdm.messages.subarray_node.configure as configure_msgs

__all__ = ['CSPConfigurationSchema',
           'FSPConfigurationSchema']


class FSPConfigurationSchema(Schema):
    """
    Marshmallow schema for the subarray_node.FSPConfiguration class
    """

    fsp_id = fields.Integer(data_key='fspID', required=True)
    function_mode = fields.String(data_key='functionMode',
                                  validate=OneOf(['CORR', 'PSS-BF', 'PST-BF', 'VLBI']),
                                  required=True)
    frequency_slice_id = fields.Integer(data_key='frequencySliceID', required=True)
    corr_bandwidth = fields.Integer(data_key='corrBandwidth', required=True)
    integration_time = fields.Integer(data_key='integrationTime', required=True)
    channel_averaging_map = fields.List(fields.Tuple((fields.Integer, fields.Integer)),
                                        data_key='channelAveragingMap')
    output_link_map = fields.List(fields.Tuple((fields.Integer, fields.Integer)),
                                  data_key='outputLinkMap')

    @pre_dump
    def convert(self, fsp_configuration: configure_msgs.FSPConfiguration,
                **_):  # pylint: disable=no-self-use
        """
        Process FSPConfiguration instance so that it is ready for conversion
        to JSON.

        :param fsp_configuration: FSP configuration to process
        :param _: kwargs passed by Marshmallow
        :return: FspConfiguration instance populated to match JSON
        """
        # Convert Python Enum to its string value
        fsp_configuration.function_mode = fsp_configuration.function_mode.value
        return fsp_configuration

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for FSP configuration
        """
        result = {k: v for k, v in data.items() if v is not None}
        return result

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a FSPConfiguration object.
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: FSPConfiguration instance populated to match JSON

        """
        fsp_id = data['fsp_id']
        function_mode = data['function_mode']
        function_mode_enum = configure_msgs.FSPFunctionMode(function_mode)
        frequency_slice_id = int(data['frequency_slice_id'])
        corr_bandwidth = data['corr_bandwidth']
        integration_time = data['integration_time']

        # optional arguments
        channel_averaging_map = data.get('channel_averaging_map', None)
        output_link_map = data.get('output_link_map', None)

        return configure_msgs.FSPConfiguration(fsp_id, function_mode_enum, frequency_slice_id,
                                               integration_time, corr_bandwidth,
                                               channel_averaging_map=channel_averaging_map,
                                               output_link_map=output_link_map)


class CSPConfigurationSchema(Schema):
    """
    Marshmallow schema for the subarray_node.CSPConfiguration class
    """
    csp_id = fields.String(data_key='id', required=True)
    frequency_band = fields.String(data_key='frequencyBand', required=True)
    fsp_configs = fields.Nested(FSPConfigurationSchema, many=True, data_key='fsp')

    @pre_dump
    def convert(self, csp_configuration: configure_msgs.CSPConfiguration,
                **_):  # pylint: disable=no-self-use
        """
        Process CSPConfiguration instance so that it is ready for conversion
        to JSON.

        :param csp_configuration: CSP configuration to process
        :param _: kwargs passed by Marshmallow
        :return: CSPConfiguration instance populated to match JSON
        """
        # Convert Python Enum to its string value
        csp_configuration.frequency_band = csp_configuration.frequency_band.value
        return csp_configuration


    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a CSPConfiguration object.
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: CSPConfiguration instance populated to match JSON

        """
        csp_id = data['csp_id']
        frequency_band = data['frequency_band']
        frequency_band_enum = configure_msgs.ReceiverBand(frequency_band)
        fsp_configs = data['fsp_configs']

        return configure_msgs.CSPConfiguration(csp_id, frequency_band_enum, fsp_configs)

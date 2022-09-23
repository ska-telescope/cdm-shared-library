"""
The releaseresources module defines Marshmallow schemas that map
MCCSController ReleaseResourcesRequest objects to/from their JSON
representation.
"""
from marshmallow import fields, post_load, post_dump

from ska_tmc_cdm.messages.mccscontroller.releaseresources import ReleaseResourcesRequest
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.schemas.shared import ValidatingSchema


@CODEC.register_mapping(ReleaseResourcesRequest)
class ReleaseResourcesRequestSchema(
    ValidatingSchema
):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the ReleaseResourcesRequest class.
    """

    interface = fields.String(required=True)
    subarray_id = fields.Integer(required=True)
    release_all = fields.Boolean(required=True)
    subarray_beam_ids = fields.List(fields.Integer)
    channels = fields.List(fields.List(fields.Integer))

    @post_dump
    def filter_args(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter Marshmallow's JSON based on the value of release_all.

        If release_all is True, other resource definitions should be stripped
        from the request.
        If release_all for MID set to False, the 'release_all' key
        itself should be stripped.
        If release_all_low for LOW set to False, the 'release_all_low' key
        itself should be stripped.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for request submission
        """
  

        # Filter out  null values from JSON.
        data = {k: v for k, v in data.items() if v is not None}

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
        interface = data["interface"]
        subarray_id = data["subarray_id"]
        release_all = data["release_all"]
        subarray_beam_ids = data.get("subarray_beam_ids",None)
        channels = data.get("channels",None)
        return ReleaseResourcesRequest(
            interface=interface, subarray_id=subarray_id, release_all=release_all, subarray_beam_ids=subarray_beam_ids, 
            channels=channels
        )

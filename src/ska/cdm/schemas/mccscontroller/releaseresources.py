"""
The releaseresources module defines Marshmallow schemas that map
MCCSController ReleaseResourcesRequest objects to/from their JSON
representation.
"""
from marshmallow import Schema, fields, post_load

from ska.cdm.messages.mccscontroller.releaseresources import ReleaseResourcesRequest
from ska.cdm.schemas import CODEC


@CODEC.register_mapping(ReleaseResourcesRequest)
class ReleaseResourcesRequestSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the ReleaseResourcesRequest class.
    """

    interface = fields.String(required=True)
    subarray_id = fields.Integer(required=True)
    release_all = fields.Boolean(required=True)

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
        return ReleaseResourcesRequest(
            interface=interface,
            subarray_id=subarray_id,
            release_all=release_all
        )

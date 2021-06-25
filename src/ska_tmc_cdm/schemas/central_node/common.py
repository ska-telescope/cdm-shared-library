"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_load

from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.schemas import CODEC

__all__ = ["DishAllocationSchema", "DishAllocationResponseSchema"]


@CODEC.register_mapping(DishAllocation)
class DishAllocationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the DishAllocation class.
    """

    receptor_ids = fields.List(
        fields.String, data_key="receptor_ids", many=True, required=True
    )

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a DishAllocation object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: DishAllocation object populated from data
        """
        receptor_ids = data["receptor_ids"]
        return DishAllocation(receptor_ids=receptor_ids)


@CODEC.register_mapping(DishAllocation)
class DishAllocationResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the DishAllocation class when received in the
    response.
    """

    receptor_ids = fields.List(
        fields.String, data_key="receptor_ids_success", many=True, required=True
    )

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
        receptor_ids = data["receptor_ids"]
        return DishAllocation(receptor_ids=receptor_ids)

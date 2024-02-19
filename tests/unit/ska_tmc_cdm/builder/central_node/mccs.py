from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate


class MCCSAllocateBuilder:
    """
    MCCSAllocateBuilder is a test data builder for CDM MCCSAllocate objects.

    By default, MCCSAllocateBuilder will build an MCCSAllocate

    for low observation command.
    """

    def __init__(self) -> "MCCSAllocateBuilder":
        self.subarray_beam_ids = None
        self.channel_blocks = None
        self.station_ids = None

    def set_subarray_beam_ids(self, subarray_beam_ids: list) -> "MCCSAllocateBuilder":
        """
        Set subarray_beam_ids
        :param subarray_beam_ids: subarray_beam_ids
        """
        self.subarray_beam_ids = subarray_beam_ids
        return self

    def set_station_ids(self, station_ids: list) -> "MCCSAllocateBuilder":
        """
        Set station_ids
        :param station_ids: station_ids
        """
        self.station_ids = station_ids
        return self

    def set_channel_blocks(self, channel_blocks: list) -> "MCCSAllocateBuilder":
        """
        Set channel_blocks
        :param channel_blocks: channel_blocks
        """
        self.channel_blocks = channel_blocks
        return self

    def build(self) -> MCCSAllocate:
        """
        Build or create CDM MCCSAllocate object
        :return: CDM MCCSAllocate object
        """
        return MCCSAllocate(
            subarray_beam_ids=self.subarray_beam_ids,
            station_ids=self.station_ids,
            channel_blocks=self.channel_blocks,
        )

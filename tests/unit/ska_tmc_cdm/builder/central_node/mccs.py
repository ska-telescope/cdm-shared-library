from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate

"""
MCCSAllocateBuilder is a test data builder for CDM MCCSAllocate objects.

By default, MCCSAllocateBuilder will build an MCCSAllocate

for low observation command.
"""


class MCCSAllocateBuilder:
    def __init__(self) ->  "MCCSAllocateBuilder":
        self.mccs = None
        self.subarray_beam_ids = None
        self.channel_blocks = None
        self.station_ids = None

    def set_subarray_beam_ids(self, subarray_beam_ids=list) -> "MCCSAllocateBuilder":
        self.subarray_beam_ids = subarray_beam_ids
        return self

    def set_station_ids(self, station_ids=list) -> "MCCSAllocateBuilder":
        self.station_ids = station_ids
        return self

    def set_channel_blocks(self, channel_blocks=list) -> "MCCSAllocateBuilder":
        self.channel_blocks = channel_blocks
        return self

    def build(self) -> MCCSAllocate:
        self.mccs = MCCSAllocate(
            subarray_beam_ids=self.subarray_beam_ids,
            station_ids=self.station_ids,
            channel_blocks=self.channel_blocks,
        )
        return self.mccs

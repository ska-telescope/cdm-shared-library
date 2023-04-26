from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate

"""
MCCSAllocateBuilder is a test data builder for CDM MCCSAllocate objects.

By default, MCCSAllocateBuilder will build an MCCSAllocate

for low observation command.
"""


class MCCSAllocateBuilder:
    def __init__(
        self,
        mccs=MCCSAllocate(
            subarray_beam_ids=list(), station_ids=list(), channel_blocks=list(list())
        ),
    ) -> object:
        self.mccs = mccs
        self.subarray_beam_ids = mccs.subarray_beam_ids
        self.station_ids = mccs.station_ids
        self.channel_block = mccs.channel_blocks

    def set_subarray_beam_ids(self, subarray_beam_ids):
        self.mccs.subarray_beam_ids = subarray_beam_ids
        return self

    def set_station_ids(self, station_ids):
        self.mccs.station_ids = station_ids
        return self

    def set_channel_blocks(self, channel_blocks):
        self.mccs.channel_blocks = channel_blocks
        return self

    def build(self):
        return self.mccs

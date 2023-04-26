from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate

"""
MCCSAllocateBuilder is a test data builder for CDM MCCSAllocate objects.

By default, MCCSAllocateBuilder will build an MCCSAllocate

for low observation command.
"""


class MCCSAllocateBuilder:
    def __init__(self) -> object:
        self.mccs = None

    def set_subarray_beam_ids(self, subarray_beam_ids):
        self.subarray_beam_ids = subarray_beam_ids
        return self

    def set_station_ids(self, station_ids):
        self.station_ids = station_ids
        return self

    def set_channel_blocks(self, channel_blocks):
        self.channel_blocks = channel_blocks
        return self

    def build(self):
        self.mccs = MCCSAllocate(
            subarray_beam_ids=self.subarray_beam_ids,
            station_ids=self.station_ids,
            channel_blocks=self.channel_blocks,
        )
        return self.mccs

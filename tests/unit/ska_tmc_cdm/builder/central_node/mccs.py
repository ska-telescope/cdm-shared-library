from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate

"""
Create a sdp block using builder pattern
"""

class MCCSAllocateBuilder:
    def __init__(
        self,
        mccs=MCCSAllocate(
            subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
        ),
    ):
        self.mccs = mccs

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

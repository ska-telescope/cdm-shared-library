import functools

from ska_tmc_cdm.messages.subarray_node.configure.sdp import (
    SDP_SCHEMA,
    SDPConfiguration,
)

SDPConfigurationBuilder = functools.partial(
    SDPConfiguration, interface=SDP_SCHEMA, scan_type="science_A"
)

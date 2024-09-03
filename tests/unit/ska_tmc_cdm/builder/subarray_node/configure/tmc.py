import functools
from datetime import timedelta

from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration

TMCConfigurationBuilder = functools.partial(
    TMCConfiguration,
    scan_duration=timedelta(seconds=10),
    partial_configuration=False,
)

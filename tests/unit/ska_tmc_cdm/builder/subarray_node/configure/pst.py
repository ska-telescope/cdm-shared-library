import functools
from typing import List

from ska_tmc_cdm.messages.subarray_node.configure.pst import (
    PSTBeamConfiguration,
    PSTChannelizationStageConfiguration,
    PSTConfiguration,
    PSTScanConfiguration,
    PSTScanCoordinates,
)

PSTScanCoordinatesBuilder = functools.partial(PSTScanCoordinates)

PSTChannelizationStageConfigurationBuilder = functools.partial(
    PSTChannelizationStageConfiguration
)
PSTScanConfigurationBuilder = functools.partial(PSTScanConfiguration)
PSTBeamConfigurationBuilder = functools.partial(PSTBeamConfiguration)
PSTConfigurationBuilder = functools.partial(PSTConfiguration)

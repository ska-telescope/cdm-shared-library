import functools
from typing import List, Tuple

from ska_tmc_cdm.messages.subarray_node.configure import core
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    BeamsConfiguration,
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    LowCBFConfiguration,
    PSSConfiguration,
    PSTConfiguration,
    StationConfiguration,
    StnBeamConfiguration,
    SubarrayConfiguration,
    TimingBeamsConfiguration,
    VisConfiguration,
    VisFspConfiguration,
    VisStnBeamConfiguration,
)

FSPConfigurationBuilder = functools.partial(FSPConfiguration)

SubarrayConfigurationBuilder = functools.partial(SubarrayConfiguration)

CommonConfigurationBuilder = functools.partial(CommonConfiguration)

CBFConfigurationBuilder = functools.partial(CBFConfiguration)

BeamsConfigurationBuilder = functools.partial(BeamsConfiguration)

TimingBeamsConfigurationBuilder = functools.partial(TimingBeamsConfiguration)

LowCBFConfigurationBuilder = functools.partial(LowCBFConfiguration)

StationConfigurationBuilder = functools.partial(StationConfiguration)

StnBeamConfigurationBuilder = functools.partial(StnBeamConfiguration)

VisFspConfigurationBuilder = functools.partial(VisFspConfiguration)

VisStnBeamConfigurationBuilder = functools.partial(VisStnBeamConfiguration)

VisConfigurationBuilder = functools.partial(VisConfiguration)

CSPConfigurationBuilder = functools.partial(CSPConfiguration)

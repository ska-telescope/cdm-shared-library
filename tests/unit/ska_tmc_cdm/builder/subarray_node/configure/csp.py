import functools
from typing import List, Tuple

from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
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

FSPConfigurationBuilder = functools.partial(
    FSPConfiguration,
    fsp_id=1,
    function_mode=FSPFunctionMode.CORR,
    frequency_slice_id=1,
    integration_factor=10,
    zoom_factor=0,
)


SubarrayConfigurationBuilder = functools.partial(
    SubarrayConfiguration, subarray_name="Test Subarray"
)

CommonConfigurationBuilder = functools.partial(
    CommonConfiguration,
    config_id="sbi-mvp01-20200325-00001-science_A",
    frequency_band=ReceiverBand.BAND_1,
    subarray_id=1,
    band_5_tuning=(5.85, 7.25),
)


CBFConfigurationBuilder = functools.partial(CBFConfiguration)

BeamsConfigurationBuilder = functools.partial(BeamsConfiguration)

TimingBeamsConfigurationBuilder = functools.partial(TimingBeamsConfiguration)

LowCBFConfigurationBuilder = functools.partial(LowCBFConfiguration)

StationConfigurationBuilder = functools.partial(StationConfiguration)

StnBeamConfigurationBuilder = functools.partial(StnBeamConfiguration,
            stn_beam_id=1¸
            beam_id=1,
            freq_ids=(400,),
            delay_poly="tango/device/instance/delay",)

VisFspConfigurationBuilder = functools.partial(VisFspConfiguration)

VisStnBeamConfigurationBuilder = functools.partial(VisStnBeamConfiguration)

VisConfigurationBuilder = functools.partial(VisConfiguration)

CSPConfigurationBuilder = functools.partial(CSPConfiguration)

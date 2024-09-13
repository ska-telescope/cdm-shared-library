import functools

from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    BeamsConfiguration,
    CBFConfigurationDeprecated,
    CommonConfiguration,
    CorrelationConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    LowCBFConfiguration,
    ProcessingRegionConfiguration,
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
    frequency_band=ReceiverBand.BAND_5A,
    subarray_id=1,
    band_5_tuning=(5.85, 7.25),
)


CBFConfigurationBuilder = functools.partial(
    CBFConfigurationDeprecated, fsp=[FSPConfigurationBuilder()]
)

BeamsConfigurationBuilder = functools.partial(
    BeamsConfiguration,
    pst_beam_id=1,
    stn_beam_id=1,
    stn_weights=(0.9, 1.0, 1.0, 1.0, 0.9, 1.0),
)

StnBeamConfigurationBuilder = functools.partial(
    StnBeamConfiguration,
    stn_beam_id=1,
    beam_id=1,
    freq_ids=(400,),
    delay_poly="tango/device/instance/delay",
)

StationConfigurationBuilder = functools.partial(
    StationConfiguration,
    stns=((1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)),
    stn_beams=(StnBeamConfigurationBuilder(),),
)

VisFspConfigurationBuilder = functools.partial(
    VisFspConfiguration,
    function_mode="vis",
    fsp_ids=(1, 2),
    firmware="pst",
)

VisStnBeamConfigurationBuilder = functools.partial(
    VisStnBeamConfiguration,
    stn_beam_id=1,
    # Note: tuples for test isolation
    host=((0, "192.168.1.00"),),
    port=((0, 9000, 1),),
    mac=((0, "02-03-04-0a-0b-0c"),),
    integration_ms=849,
)

VisConfigurationBuilder = functools.partial(
    VisConfiguration,
    fsp=VisFspConfigurationBuilder(),
    stn_beams=(VisStnBeamConfigurationBuilder(),),
)

TimingBeamsConfigurationBuilder = functools.partial(
    TimingBeamsConfiguration,
    beams=(BeamsConfigurationBuilder(),),
    fsp=VisFspConfigurationBuilder(),
)

CSPConfigurationBuilder = functools.partial(
    CSPConfiguration,
    interface="interface",
    subarray=SubarrayConfigurationBuilder(),
    common=CommonConfigurationBuilder(),
    cbf_config=CBFConfigurationBuilder(),
)

LowCBFConfigurationBuilder = functools.partial(
    LowCBFConfiguration,
    stations=StationConfigurationBuilder(),
    vis=VisConfigurationBuilder(),
    timing_beams=TimingBeamsConfigurationBuilder(),
)

ProcessingRegionConfigurationBuilder = functools.partial(
    ProcessingRegionConfiguration, fsp_ids=(1, 2, 3), start_freq=5
)

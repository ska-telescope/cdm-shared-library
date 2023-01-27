"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.csp module.
"""
import copy
import functools
import itertools

import pytest

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
    StationsConfiguration,
    StnBeamConfiguration,
    SubarrayConfiguration,
    TimingBeamsConfiguration,
)

CONSTRUCTOR_ARGS = dict(
    interface="interface",
    subarray=SubarrayConfiguration(subarray_name="subarray name"),
    common=CommonConfiguration(
        config_id="config_id",
        frequency_band=ReceiverBand.BAND_1,
        subarray_id=1,
        band_5_tuning=[5.85, 7.25],
    ),
    cbf_config=CBFConfiguration(
        fsp_configs=[FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)]
    ),
    pss_config=None,
    pst_config=None,
)

CSP_CONFIGURATION_ARGS_PI16 = dict(
    interface="https://schema.skao.int/ska-csp-configure/2.0",
    subarray=SubarrayConfiguration("science period 23"),
    common=CommonConfiguration(
        config_id="sbi-mvp01-20200325-00001-science_A",
        frequency_band=ReceiverBand.BAND_1,
        subarray_id=1,
    ),
    pss_config={},
    pst_config={},
    cbf_config=CBFConfiguration(
        fsp_configs=[
            FSPConfiguration(
                fsp_id=1,
                function_mode=FSPFunctionMode.CORR,
                frequency_slice_id=1,
                integration_factor=1,
                zoom_factor=0,
                channel_averaging_map=[(0, 2), (744, 0)],
                channel_offset=0,
                output_link_map=[(0, 0), (200, 1)],
            ),
            FSPConfiguration(
                fsp_id=2,
                function_mode=FSPFunctionMode.CORR,
                frequency_slice_id=2,
                integration_factor=1,
                zoom_factor=1,
                channel_averaging_map=[(0, 2), (744, 0)],
                channel_offset=744,
                output_link_map=[(0, 4), (200, 5)],
                zoom_window_tuning=650000,
            ),
        ],
        vlbi_config={},
    ),
)


def test_commonuration_equals():
    """
    Verify that CommonConfiguration objects are considered equal when all
    attributes are equal.
    """
    config_id = "sbi-mvp01-20200325-00001-science_A"
    frequency_band = ReceiverBand.BAND_1
    subarray_id = 1
    band_5_tuning = [5.85, 7.25]

    config1 = CommonConfiguration(config_id, frequency_band, subarray_id, band_5_tuning)
    config2 = CommonConfiguration(config_id, frequency_band, subarray_id, band_5_tuning)
    assert config1 == config2

    assert config1 != CommonConfiguration(
        config_id, ReceiverBand.BAND_2, subarray_id, band_5_tuning
    )
    assert config1 != CommonConfiguration(config_id, frequency_band, 2, band_5_tuning)
    assert config1 != CommonConfiguration(config_id, frequency_band, 2)


def test_commonuration_not_equal_to_other_objects():
    """
    Verify that CommonConfiguration objects are not considered equal to objects
    of other types.
    """
    config_id = "sbi-mvp01-20200325-00001-science_A"
    frequency_band = ReceiverBand.BAND_1
    subarray_id = 1
    band_5_tuning = [5.85, 7.25]
    config = CommonConfiguration(config_id, frequency_band, subarray_id, band_5_tuning)
    assert config != 1


def test_subarray_configuration_equals():
    """
    Verify that SubarrayConfiguration objects are considered equal when all
    attributes are equal.
    """
    subarray_name = "Test Subarray"

    config1 = SubarrayConfiguration(subarray_name)
    config2 = SubarrayConfiguration(subarray_name)
    assert config1 == config2

    assert config1 != SubarrayConfiguration("Test Subarray2")


def test_subarray_configuration_not_equal_to_other_objects():
    """
    Verify that SubarrayConfiguration objects are not considered equal to objects
    of other types.
    """
    subarray_name = "Test Subarray"
    config = SubarrayConfiguration(subarray_name)
    assert config != 1


def test_cbf_configuration_equals():
    """
    Verify that CBFConfiguration objects are considered equal when all
    attributes are equal.
    """
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)

    config1 = CBFConfiguration([fsp])
    config2 = CBFConfiguration([fsp])
    assert config1 == config2

    assert config1 != CBFConfiguration([fsp, fsp])


def test_cbf_configuration_not_equal_to_other_objects():
    """
    Verify that CBFConfiguration objects are not considered equal to objects
    of other types.
    """
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)
    config = CBFConfiguration([fsp])
    assert config != 1


def test_fsp_configuration_equals():
    """
    Verify that FSPConfigurations are considered equal when all attributes are
    equal.
    """
    fsp_id = 1
    mode = FSPFunctionMode.CORR
    slice_id = 1
    zoom_factor = 0
    channel_avg_map = list(zip(itertools.count(1, 744), 20 * [0]))
    integration_factor = 10

    config1 = FSPConfiguration(
        fsp_id, mode, slice_id, integration_factor, zoom_factor, channel_avg_map
    )
    config2 = FSPConfiguration(
        fsp_id, mode, slice_id, integration_factor, zoom_factor, channel_avg_map
    )
    assert config1 == config2

    assert config1 != FSPConfiguration(
        2, mode, slice_id, integration_factor, zoom_factor, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id,
        FSPFunctionMode.PSS_BF,
        slice_id,
        integration_factor,
        zoom_factor,
        channel_avg_map,
    )
    assert config1 != FSPConfiguration(
        fsp_id, mode, 2, integration_factor, zoom_factor, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id, mode, slice_id, 2, zoom_factor, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id, mode, slice_id, integration_factor, 1, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id,
        mode,
        slice_id,
        integration_factor,
        zoom_factor,
        list(zip(itertools.count(1, 744), 20 * [1])),
    )


def test_fsp_configuration_not_equal_to_other_objects():
    """
    Verify that FSPConfiguration objects are not considered equal to objects
    of other types.
    """
    config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)
    assert config != 1


def test_csp_configuration_equals():
    """
    Verify that CSPConfiguration objects are considered equal when all
    attributes are equal.
    """
    o = CSPConfiguration(**CONSTRUCTOR_ARGS)
    assert o == copy.deepcopy(o)

    alt_constructor_args = dict(
        interface="foo",
        subarray=SubarrayConfiguration(subarray_name="foo"),
        common=CommonConfiguration(
            config_id="foo",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1,
            band_5_tuning=[5.85, 7.25],
        ),
        cbf_config=CBFConfiguration(
            fsp_configs=[FSPConfiguration(2, FSPFunctionMode.CORR, 1, 10, 0)]
        ),
        pss_config=PSSConfiguration(),
        pst_config=PSTConfiguration(),
        lowcbf=LowCBFConfiguration(
            stations=StationsConfiguration(
                stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
                stn_beams=StnBeamConfiguration(
                    beam_id=1,
                    freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
                    boresight_dly_poly="url",
                ),
            ),
            timing_beams=TimingBeamsConfiguration(
                beams=BeamsConfiguration(
                    pst_beam_id=13,
                    stn_beam_id=1,
                    offset_dly_poly="url",
                    stn_weights=[0.9, 1.0, 1.0, 0.9],
                    jones="url",
                    dest_ip=["10.22.0.1:2345", "10.22.0.3:3456"],
                    dest_chans=[128, 256],
                    rfi_enable=[True, True, True],
                    rfi_static_chans=[1, 206, 997],
                    rfi_dynamic_chans=[242, 1342],
                    rfi_weighted=0.87,
                )
            ),
        ),
    )

    for k, v in alt_constructor_args.items():
        alt_args = dict(CONSTRUCTOR_ARGS)
        alt_args[k] = v
        other = CSPConfiguration(**alt_args)
        assert o != other


def test_csp_configuration_not_equal_to_other_objects():
    """
    Verify that CSPConfiguration objects are not considered equal to objects
    of other types.
    """
    o = CSPConfiguration(**CONSTRUCTOR_ARGS)
    assert o != 1


def test_csp_configuration_objects_are_equal_pi16():
    """
    Verify that CSPConfiguration objects are considered equal when all
    attributes are equal.
    """

    csp_obj_1 = CSPConfiguration(**CSP_CONFIGURATION_ARGS_PI16)
    csp_obj_2 = CSPConfiguration(**CSP_CONFIGURATION_ARGS_PI16)

    assert csp_obj_1 == csp_obj_2

    alt_csp_configuration_csp_2_0_args = CSP_CONFIGURATION_ARGS_PI16.copy()
    alt_csp_configuration_csp_2_0_args[
        "interface"
    ] = "Changing interface value for creating object with different value"

    csp_obj_3 = CSPConfiguration(**alt_csp_configuration_csp_2_0_args)

    assert csp_obj_1 != csp_obj_3


def test_csp_configuration_not_equal_to_other_objects_pi16():
    """
    Verify that CSPConfiguration objects are not considered equal to objects
    of other types.
    """
    csp_obj_1 = CSPConfiguration(**CSP_CONFIGURATION_ARGS_PI16)

    assert csp_obj_1 != 1


def test_fsp_id_range():
    """
    Verify that fsp id is in the range of 1 to 27
    """
    fsp_id = 0
    with pytest.raises(ValueError):
        _ = FSPConfiguration(fsp_id, FSPFunctionMode.CORR, 1, 140, 0)
    fsp_id = 28
    with pytest.raises(ValueError):
        _ = FSPConfiguration(fsp_id, FSPFunctionMode.CORR, 1, 140, 0)


def test_fsp_slice_id_range():
    """
    Verify that fsp slice id is in the range of 1 to 26
    """
    fsp_slice_id = 0
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, fsp_slice_id, 140, 0)
    fsp_slice_id = 27
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, fsp_slice_id, 140, 0)


def test_zoom_factor_range():
    """
    Verify that zoom_factor is in the range of 0 to 6
    """
    zoom_factor = -1
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, zoom_factor)
    zoom_factor = 7
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, zoom_factor)


def test_integration_factor_range():
    """
    Verify that integration factor is within range 1..10
    """
    _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 0, 0)
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 11, 0)


def test_number_of_channel_avg_mapping_tuples():
    """
    Verify that FSPConfiguration fails if there are an invalid number of
    entries in the channel average mapping argument.
    Since this test was originally written we allow fewer than 20 entries
    """
    # create a partially applied sn.FSPConfiguration constructor to save having
    # to type the arguments each time
    fsp_constructor = functools.partial(
        FSPConfiguration, 1, FSPFunctionMode.CORR, 1, 140, 0
    )

    # test for 21 tuples
    channel_avg_map = list(zip(itertools.count(1, 744), 21 * [0]))
    with pytest.raises(ValueError):
        _ = fsp_constructor(channel_avg_map)


def test_stn_beam_configuration_equals():
    """
    Verify that StnBeamConfiguration objects are considered equal when all
    attributes are equal.
    """
    config1 = StnBeamConfiguration(
        beam_id=1, freq_ids=[64, 65, 66, 67, 68, 68, 70, 71], boresight_dly_poly="url"
    )
    config2 = StnBeamConfiguration(
        beam_id=1, freq_ids=[64, 65, 66, 67, 68, 68, 70, 71], boresight_dly_poly="url"
    )
    assert config1 == config2

    assert config1 != StnBeamConfiguration(beam_id=1)


def test_stn_beam_configuration_not_equal_to_other_objects():
    """
    Verify that StnBeamConfiguration objects are not considered equal to objects
    of other types.
    """
    config = StnBeamConfiguration(
        beam_id=1, freq_ids=[64, 65, 66, 67, 68, 68, 70, 71], boresight_dly_poly="url"
    )
    assert config != 1


def test_station_configuration_equals():
    """
    Verify that StationsConfiguration objects are considered equal when all
    attributes are equal.
    """

    config1 = StationsConfiguration(
        stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
        stn_beams=StnBeamConfiguration(
            beam_id=1,
            freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
            boresight_dly_poly="url",
        ),
    )
    config2 = StationsConfiguration(
        stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
        stn_beams=StnBeamConfiguration(
            beam_id=1,
            freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
            boresight_dly_poly="url",
        ),
    )
    assert config1 == config2

    assert config1 != StationsConfiguration(stns=[[1, 0], [2, 0], [3, 0], [4, 0]])


def test_station_configuration_not_equal_to_other_objects():
    """
    Verify that StationsConfiguration objects are not considered equal to objects
    of other types.
    """

    config = StationsConfiguration(
        stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
        stn_beams=StnBeamConfiguration(
            beam_id=1,
            freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
            boresight_dly_poly="url",
        ),
    )
    assert config != 1


def test_beams_configuration_equals():
    """
    Verify that BeamsConfiguration objects are considered equal when all
    attributes are equal.
    """

    config1 = BeamsConfiguration(
        pst_beam_id=13,
        stn_beam_id=1,
        offset_dly_poly="url",
        stn_weights=[0.9, 1.0, 1.0, 0.9],
        jones="url",
        dest_ip=["10.22.0.1:2345", "10.22.0.3:3456"],
        dest_chans=[128, 256],
        rfi_enable=[True, True, True],
        rfi_static_chans=[1, 206, 997],
        rfi_dynamic_chans=[242, 1342],
        rfi_weighted=0.87,
    )
    config2 = BeamsConfiguration(
        pst_beam_id=13,
        stn_beam_id=1,
        offset_dly_poly="url",
        stn_weights=[0.9, 1.0, 1.0, 0.9],
        jones="url",
        dest_ip=["10.22.0.1:2345", "10.22.0.3:3456"],
        dest_chans=[128, 256],
        rfi_enable=[True, True, True],
        rfi_static_chans=[1, 206, 997],
        rfi_dynamic_chans=[242, 1342],
        rfi_weighted=0.87,
    )
    assert config1 == config2
    assert config1 != BeamsConfiguration(pst_beam_id=13)


def test_beams_configuration_not_equal_to_other_objects():
    """
    Verify that BeamConfiguration objects are not considered equal to objects
    of other types.
    """

    config = BeamsConfiguration(
        BeamsConfiguration(
            pst_beam_id=13,
            stn_beam_id=1,
            offset_dly_poly="url",
            stn_weights=[0.9, 1.0, 1.0, 0.9],
            jones="url",
            dest_ip=["10.22.0.1:2345", "10.22.0.3:3456"],
            dest_chans=[128, 256],
            rfi_enable=[True, True, True],
            rfi_static_chans=[1, 206, 997],
            rfi_dynamic_chans=[242, 1342],
            rfi_weighted=0.87,
        )
    )
    assert config != 1


def test_timing_beams_configuration_equals():
    """
    Verify that TimingBeamsConfiguration objects are considered equal when all
    attributes are equal.
    """

    config1 = TimingBeamsConfiguration(
        beams=BeamsConfiguration(
            pst_beam_id=13,
            stn_beam_id=1,
            offset_dly_poly="url",
            stn_weights=[0.9, 1.0, 1.0, 0.9],
            jones="url",
            dest_ip=["10.22.0.1:2345", "10.22.0.3:3456"],
            dest_chans=[128, 256],
            rfi_enable=[True, True, True],
            rfi_static_chans=[1, 206, 997],
            rfi_dynamic_chans=[242, 1342],
            rfi_weighted=0.87,
        )
    )
    config2 = TimingBeamsConfiguration(
        beams=BeamsConfiguration(
            pst_beam_id=13,
            stn_beam_id=1,
            offset_dly_poly="url",
            stn_weights=[0.9, 1.0, 1.0, 0.9],
            jones="url",
            dest_ip=["10.22.0.1:2345", "10.22.0.3:3456"],
            dest_chans=[128, 256],
            rfi_enable=[True, True, True],
            rfi_static_chans=[1, 206, 997],
            rfi_dynamic_chans=[242, 1342],
            rfi_weighted=0.87,
        )
    )
    assert config1 == config2
    assert config1 != TimingBeamsConfiguration(beams=BeamsConfiguration(pst_beam_id=13))


def test_timing_beams_configuration_not_equal_to_other_objects():
    """
    Verify that TimingBeamsConfiguration objects are not considered equal to objects
    of other types.
    """
    config = TimingBeamsConfiguration(
        beams=BeamsConfiguration(
            pst_beam_id=13,
            stn_beam_id=1,
            offset_dly_poly="url",
            stn_weights=[0.9, 1.0, 1.0, 0.9],
            jones="url",
            dest_ip=["10.22.0.1:2345", "10.22.0.3:3456"],
            dest_chans=[128, 256],
            rfi_enable=[True, True, True],
            rfi_static_chans=[1, 206, 997],
            rfi_dynamic_chans=[242, 1342],
            rfi_weighted=0.87,
        )
    )
    assert config != 1


def test_low_cbf_configuration_equals():
    """
    Verify that LowCBFConfiguration objects are considered equal when all
    attributes are equal.
    """

    config1 = LowCBFConfiguration(
        stations=StationsConfiguration(
            stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
            stn_beams=StnBeamConfiguration(
                beam_id=1,
                freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
                boresight_dly_poly="url",
            ),
        ),
        timing_beams=TimingBeamsConfiguration(
            beams=BeamsConfiguration(
                pst_beam_id=13,
                stn_beam_id=1,
                offset_dly_poly="url",
                stn_weights=[0.9, 1.0, 1.0, 0.9],
                jones="url",
                dest_ip=["10.22.0.1:2345", "10.22.0.3:3456"],
                dest_chans=[128, 256],
                rfi_enable=[True, True, True],
                rfi_static_chans=[1, 206, 997],
                rfi_dynamic_chans=[242, 1342],
                rfi_weighted=0.87,
            )
        ),
    )
    config2 = LowCBFConfiguration(
        stations=StationsConfiguration(
            stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
            stn_beams=StnBeamConfiguration(
                beam_id=1,
                freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
                boresight_dly_poly="url",
            ),
        ),
        timing_beams=TimingBeamsConfiguration(
            beams=BeamsConfiguration(
                pst_beam_id=13,
                stn_beam_id=1,
                offset_dly_poly="url",
                stn_weights=[0.9, 1.0, 1.0, 0.9],
                jones="url",
                dest_ip=["10.22.0.1:2345", "10.22.0.3:3456"],
                dest_chans=[128, 256],
                rfi_enable=[True, True, True],
                rfi_static_chans=[1, 206, 997],
                rfi_dynamic_chans=[242, 1342],
                rfi_weighted=0.87,
            )
        ),
    )
    assert config1 == config2
    assert config1 != LowCBFConfiguration(
        stations=StationsConfiguration(
            stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
            stn_beams=StnBeamConfiguration(
                beam_id=1,
                freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
                boresight_dly_poly="url",
            ),
        )
    )


def test_low_cbf_configuration_not_equal_to_other_objects():
    """
    Verify that LowCBFConfiguration objects are not considered equal to objects
    of other types.
    """

    config = LowCBFConfiguration(
        stations=StationsConfiguration(
            stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
            stn_beams=StnBeamConfiguration(
                beam_id=1,
                freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
                boresight_dly_poly="url",
            ),
        ),
        timing_beams=TimingBeamsConfiguration(
            beams=BeamsConfiguration(
                pst_beam_id=13,
                stn_beam_id=1,
                offset_dly_poly="url",
                stn_weights=[0.9, 1.0, 1.0, 0.9],
                jones="url",
                dest_ip=["10.22.0.1:2345", "10.22.0.3:3456"],
                dest_chans=[128, 256],
                rfi_enable=[True, True, True],
                rfi_static_chans=[1, 206, 997],
                rfi_dynamic_chans=[242, 1342],
                rfi_weighted=0.87,
            )
        ),
    )
    assert config != 1

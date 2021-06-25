"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.csp module.
"""
import functools
import itertools

import copy
import pytest

from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    PSSConfiguration,
    PSTConfiguration,
    SubarrayConfiguration,
)


CONSTRUCTOR_ARGS = dict(
    interface="interface",
    subarray_config=SubarrayConfiguration(
        subarray_name="subarray name"
    ),
    common_config=CommonConfiguration(
        config_id="config_id",
        frequency_band=ReceiverBand.BAND_1,
        subarray_id=1
    ),
    cbf_config=CBFConfiguration(
        fsp_configs=[
           FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)
        ]
    ),
    pss_config=None,
    pst_config=None,
)


def test_common_configuration_equals():
    """
    Verify that CommonConfiguration objects are considered equal when all
    attributes are equal.
    """
    config_id = "sbi-mvp01-20200325-00001-science_A"
    frequency_band = ReceiverBand.BAND_1
    subarray_id = 1

    config1 = CommonConfiguration(config_id, frequency_band, subarray_id)
    config2 = CommonConfiguration(config_id, frequency_band, subarray_id)
    assert config1 == config2

    assert config1 != CommonConfiguration(config_id, ReceiverBand.BAND_2, subarray_id)
    assert config1 != CommonConfiguration(config_id, frequency_band, 2)


def test_common_configuration_not_equal_to_other_objects():
    """
    Verify that CommonConfiguration objects are not considered equal to objects
    of other types.
    """
    config_id = "sbi-mvp01-20200325-00001-science_A"
    frequency_band = ReceiverBand.BAND_1
    subarray_id = 1
    config = CommonConfiguration(config_id, frequency_band, subarray_id)
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
        subarray_config=SubarrayConfiguration(
            subarray_name="foo"
        ),
        common_config=CommonConfiguration(
            config_id="foo",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1
        ),
        cbf_config=CBFConfiguration(
            fsp_configs=[
                FSPConfiguration(2, FSPFunctionMode.CORR, 1, 10, 0)
            ]
        ),
        pss_config=PSSConfiguration(),
        pst_config=PSTConfiguration(),
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

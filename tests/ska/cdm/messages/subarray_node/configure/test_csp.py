"""
Unit tests for the ska.cdm.messages.subarray_node.configure.csp module.
"""
import functools
import itertools
import pytest

from ska.cdm.messages.subarray_node.configure.core import ReceiverBand
from ska.cdm.messages.subarray_node.configure.csp import (
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration,
    CommonConfiguration,
    CBFConfiguration
)


def test_common_configuration_equals():
    """
    Verify that CommonConfiguration objects are considered equal when all
    attributes are equal.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    frequency_band = ReceiverBand.BAND_1
    subarray_id = 1

    config1 = CommonConfiguration(csp_id, frequency_band, subarray_id)
    config2 = CommonConfiguration(csp_id, frequency_band, subarray_id)
    assert config1 == config2

    assert config1 != CommonConfiguration(csp_id, ReceiverBand.BAND_2, subarray_id)
    assert config1 != CommonConfiguration(csp_id, frequency_band, 2)


def test_common_configuration_not_equal_to_other_objects():
    """
    Verify that CommonConfiguration objects are not considered equal to objects
    of other types.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    frequency_band = ReceiverBand.BAND_1
    subarray_id = 1
    config = CommonConfiguration(csp_id, frequency_band, subarray_id)
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
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)

    config1 = CBFConfiguration([fsp])
    config2 = CBFConfiguration([fsp])
    assert config1 == config2

    assert config1 != CBFConfiguration([fsp, fsp])


def test_cbf_configuration_not_equal_to_other_objects():
    """
    Verify that CBFConfiguration objects are not considered equal to objects
    of other types.
    """
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
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
    bandwidth = 0
    channel_avg_map = list(zip(itertools.count(1, 744), 20 * [0]))
    integration_time = 140

    config1 = FSPConfiguration(
        fsp_id, mode, slice_id, integration_time, bandwidth, channel_avg_map
    )
    config2 = FSPConfiguration(
        fsp_id, mode, slice_id, integration_time, bandwidth, channel_avg_map
    )
    assert config1 == config2

    assert config1 != FSPConfiguration(
        2, mode, slice_id, integration_time, bandwidth, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id,
        FSPFunctionMode.PSS_BF,
        slice_id,
        integration_time,
        bandwidth,
        channel_avg_map,
    )
    assert config1 != FSPConfiguration(
        fsp_id, mode, 2, integration_time, bandwidth, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id, mode, slice_id, 280, bandwidth, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id, mode, slice_id, integration_time, 1, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id,
        mode,
        slice_id,
        integration_time,
        bandwidth,
        list(zip(itertools.count(1, 744), 20 * [1])),
    )


def test_fsp_configuration_not_equal_to_other_objects():
    """
    Verify that FSPConfiguration objects are not considered equal to objects
    of other types.
    """
    config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    assert config != 1


def test_csp_configuration_equals():
    """
    Verify that CSPConfiguration objects are considered equal when all
    attributes are equal.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    frequency_band = ReceiverBand.BAND_1
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)

    config1 = CSPConfiguration(csp_id, frequency_band, [fsp])
    config2 = CSPConfiguration(csp_id, frequency_band, [fsp])
    assert config1 == config2

    assert config1 != CSPConfiguration(csp_id, ReceiverBand.BAND_2, [fsp])
    assert config1 != CSPConfiguration(csp_id, frequency_band, [fsp, fsp])


def test_csp_configuration_equals_with_all_parameters():
    """
    Verify that CSPConfiguration objects are considered equal when all
    attributes are equal.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    frequency_band = ReceiverBand.BAND_1
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    subarray_id = 1
    subarray_name = "Test Subarray"

    interface_url = "https://schema.skatelescope.org/ska-csp-configure/1.0"
    subarray_config = SubarrayConfiguration(subarray_name)
    common_config = CommonConfiguration(csp_id, frequency_band, subarray_id)
    cbf_config = CBFConfiguration([fsp])
    pst_config = None
    pss_config = None

    config1 = CSPConfiguration(csp_id, frequency_band, [fsp])
    config2 = CSPConfiguration(csp_id, frequency_band, [fsp])

    config3 = CSPConfiguration(
        interface_url=interface_url,
        subarray_config=subarray_config,
        common_config=common_config,
        cbf_config=cbf_config,
        pst_config=pst_config,
        pss_config=pss_config)
    config4 = CSPConfiguration(
        interface_url=interface_url,
        subarray_config=subarray_config,
        common_config=common_config,
        cbf_config=cbf_config,
        pst_config=pst_config,
        pss_config=pss_config)

    assert config1 == config2
    assert config3 == config4

    assert config1 != CSPConfiguration(csp_id, ReceiverBand.BAND_2, [fsp])
    assert config3 != CSPConfiguration(
        subarray_config=subarray_config,
        common_config=common_config,
        cbf_config=cbf_config,
        pst_config=pst_config,
        pss_config=pss_config)


def test_csp_configuration_support_only_new_or_old_request_in_same_call():
    """
    Verify that CSPConfiguration objects are considered equal when all
    attributes are equal.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    frequency_band = ReceiverBand.BAND_1
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    subarray_id = 1
    subarray_name = "Test Subarray"
    interface_url = "https://schema.skatelescope.org/ska-csp-configure/1.0"

    subarray_config = SubarrayConfiguration(subarray_name)
    common_config = CommonConfiguration(csp_id, frequency_band, subarray_id)
    cbf_config = CBFConfiguration([fsp])
    pst_config = None
    pss_config = None

    with pytest.raises(ValueError):
        _ = CSPConfiguration(csp_id, frequency_band, [], interface_url,
                             subarray_config, common_config,
                             cbf_config, pst_config, pss_config)


def test_csp_configuration_not_equal_to_other_objects():
    """
    Verify that CSPConfiguration objects are not considered equal to objects
    of other types.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    frequency_band = ReceiverBand.BAND_1
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    config = CSPConfiguration(csp_id, frequency_band, [fsp])
    assert config != 1


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


def test_corr_bandwidth_range():
    """
    Verify that corr_bandwidth is in the range of 0 to 6
    """
    corr_bandwidth = -1
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, corr_bandwidth)
    corr_bandwidth = 7
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, corr_bandwidth)


def test_integration_time_must_be_multiple_of_140():
    """
    Verify that integration time is multiple of 140
    """
    _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, 0)
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 139, 0)
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 141, 0)


def test_integration_time_is_within_limits():
    """
    Verify that integration time is no greater than 1400
    """
    _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 0, 0)
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1540, 0)


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

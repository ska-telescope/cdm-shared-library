"""
The configure.csp module contains Python classes that represent the various
aspects of CSP configuration that may be specified in a SubArrayNode.configure
command.
"""
import enum
from typing import List, Tuple

from . import core

__all__ = ["CSPConfiguration", "FSPConfiguration", "FSPFunctionMode","CBFConfiguration",
           "SubarrayConfiguration", "CommonConfiguration"]


class FSPFunctionMode(enum.Enum):
    """
    FSPFunctionMode is an enumeration of the available FSP modes.
    """

    CORR = "CORR"
    PSS_BF = "PSS-BF"
    PST_BF = "PST-BF"
    VLBI = "VLBI"


class FSPConfiguration:
    """
    FSPConfiguration defines the configuration for a CSP Frequency Slice
    Processor.
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            fsp_id: int,
            function_mode: FSPFunctionMode,
            frequency_slice_id: int,
            integration_time: int,
            corr_bandwidth: int,
            channel_averaging_map: List[Tuple] = None,
            output_link_map: List[Tuple] = None,
            fsp_channel_offset: int = None,
            zoom_window_tuning: int = None
    ):
        """
        Create a new FSPConfiguration.

        Channel averaging map is an optional list of 20 x (int,int) tuples.

        :param fsp_id: FSP configuration ID [1..27]
        :param function_mode: FSP function mode
        :param frequency_slice_id: frequency slicer ID [1..26]
        :param corr_bandwidth: correlator bandwidth [0..6]
        :param integration_time: integration time in ms
        :param channel_averaging_map: Optional channel averaging map
        :param output_link_map: Optional output_link_map
        :param fsp_channel_offset: Optional fsp_channel_offset
        :param zoom_window_tuning: Optional zoom_window_tuning

        :raises ValueError: Invalid parameter values entered
        """

        if not 1 <= fsp_id <= 27:
            raise ValueError("FSP ID must be in range 1..27. Got {}".format(fsp_id))
        self.fsp_id = fsp_id

        self.function_mode = function_mode

        if not 1 <= frequency_slice_id <= 26:
            msg = "Frequency slice ID must be in range 1..26. Got {}" "".format(
                frequency_slice_id
            )
            raise ValueError(msg)
        self.frequency_slice_id = frequency_slice_id

        if not 0 <= corr_bandwidth <= 6:
            msg = "Correlator bandwidth must be in range 0..6. Got {}".format(
                corr_bandwidth
            )
            raise ValueError(msg)
        self.corr_bandwidth = corr_bandwidth

        if integration_time % 140:
            msg = "Integration time must be a multiple of 140. Got {}".format(
                integration_time
            )
            raise ValueError(msg)
        if not 1 <= (integration_time / 140) <= 10:
            msg = "Integration time must in range 1..10 * 140. Got {}" "".format(
                integration_time
            )
            raise ValueError(msg)
        self.integration_time = integration_time

        if channel_averaging_map and len(channel_averaging_map) > 20:
            msg = (
                "Number of tuples in channel averaging map must be 20 or fewer."
                f"Got {len(channel_averaging_map)}"
            )

            raise ValueError(msg)
        self.channel_averaging_map = channel_averaging_map

        # TODO: update enforcements for output_link_map
        self.output_link_map = output_link_map
        self.fsp_channel_offset = fsp_channel_offset
        self.zoom_window_tuning = zoom_window_tuning

    def __eq__(self, other):
        if not isinstance(other, FSPConfiguration):
            return False
        return (
                self.fsp_id == other.fsp_id
                and self.function_mode == other.function_mode
                and self.frequency_slice_id == other.frequency_slice_id
                and self.corr_bandwidth == other.corr_bandwidth
                and self.integration_time == other.integration_time
                and self.channel_averaging_map == other.channel_averaging_map
                and self.output_link_map == other.output_link_map
                and self.fsp_channel_offset == other.fsp_channel_offset
                and self.zoom_window_tuning == other.zoom_window_tuning
        )


class SubarrayConfiguration:
    """
     Class to hold the parameters relevant only for the current sub-array device.
    """

    def __init__(self, subarray_name: str):
        """
        Create  sub-array device configuration.
        :param sub-array_name: Name of the sub-array
        """
        self.subarray_name = subarray_name

    def __eq__(self, other):
        if not isinstance(other, SubarrayConfiguration):
            return False
        return (
                self.subarray_name == other.subarray_name
        )


class CommonConfiguration:
    """
     Class to hold the CSP sub-elements.
    """

    def __init__(
            self,
            csp_id: str,
            frequency_band: core.ReceiverBand,
            subarray_id: int = None,
    ):
        """
        Create a new CSPConfiguration.

        :param csp_id: an ID for CSP configuration
        :param frequency_band: the frequency band to set
        :param subarray_id: an ID of sub-array device
        """
        self.csp_id = csp_id
        self.frequency_band = frequency_band
        self.subarray_id = subarray_id

    def __eq__(self, other):
        if not isinstance(other, CommonConfiguration):
            return False
        return (
                self.csp_id == other.csp_id
                and self.frequency_band == other.frequency_band
                and self.subarray_id == other.subarray_id
        )


class VLBIConfiguration:
    pass


class CBFConfiguration:
    """
      Class to hold all FSP and VLBI configurations.
    """

    def __init__(
            self,
            fsp_configs: List[FSPConfiguration],
            vlbi_config: VLBIConfiguration = None,
    ):
        """
        Create a new CBFConfiguration.
        :param fsp_configs: the FSP configurations to set
        :param vlbi_config: the VLBI configurations to set, it is optional
        """
        self.fsp_configs = fsp_configs
        self.vlbi_config = vlbi_config

    def __eq__(self, other):
        if not isinstance(other, CBFConfiguration):
            return False
        return (
                self.fsp_configs == other.fsp_configs
                and self.vlbi_config == other.vlbi_config
        )


class PSTConfiguration:
    pass


class PSSConfiguration:
    pass


class CSPConfiguration:
    """
    Class to hold all CSP configuration.
    """

    def __init__(
            self,
            csp_id: str = None,
            frequency_band: core.ReceiverBand = None,
            fsp_configs: List[FSPConfiguration] = None,
            subarray_config: SubarrayConfiguration = None,
            common_element_config: CommonConfiguration = None,
            cbf_config: CBFConfiguration = None,
            pst_config: PSTConfiguration = None,
            pss_config: PSSConfiguration = None

    ):
        """
        Create a new CSPConfiguration, In order to support backward compatibility, We have
        kept old attributes as it is and added support of new attributes as per ADR-18

        :param csp_id: an ID for CSP configuration
        :param frequency_band: the frequency band to set
        :param fsp_configs: the FSP configurations to set
        :param subarray_config: Sub-array configuration to set
        :param common_element_config: the common CSP elemenets to set
        :param cbf_config: the CBF configurations to set
        :param pst_config: the PST configurations to set
        :param pss_config: the PSS configurations to set
        """
        self.csp_id = csp_id
        self.frequency_band = frequency_band
        self.fsp_configs = fsp_configs
        self.subarray_config = subarray_config
        self.common_element_config = common_element_config
        self.cbf_config = cbf_config
        self.pst_config = pst_config
        self.pss_config = pss_config

        if self.common_element_config is not None and (
            self.csp_id is not None or self.frequency_band is not None or self.fsp_configs is not None
        ):
            raise ValueError(
                "Can't configure old CSP and ADR-18 supported CSP attiributes in the same call"
            )

    def __eq__(self, other):
        if not isinstance(other, CSPConfiguration):
            return False
        return (
                self.csp_id == other.csp_id
                and self.frequency_band == other.frequency_band
                and self.fsp_configs == other.fsp_configs
                and self.subarray_config == other.subarray_config
                and self.common_element_config == other.common_element_config
                and self.cbf_config == other.cbf_config
                and self.pst_config == other.pst_config
                and self.pss_config == other.pss_config
        )

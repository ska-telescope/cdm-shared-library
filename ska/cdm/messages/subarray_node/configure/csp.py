"""
The configure.csp module contains Python classes that represent the various
aspects of CSP configuration that may be specified in a SubArrayNode.configure
command.
"""
import enum
from typing import List, Tuple

from .common import ReceiverBand

__all__ = ['CSPConfiguration', 'FSPConfiguration', 'FSPFunctionMode']


class FSPFunctionMode(enum.Enum):
    """
    FSPFunctionMode is an enumeration of the available FSP modes.
    """
    CORR = 'CORR'
    PSS_BF = 'PSS-BF'
    PST_BF = 'PST-BF'
    VLBI = 'VLBI'


class FSPConfiguration:
    """
    FSPConfiguration defines the configuration for a CSP Frequency Slice
    Processor.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, fsp_id: int, function_mode: FSPFunctionMode, frequency_slice_id: int,
                 integration_time: int, corr_bandwidth: int,
                 channel_averaging_map: List[Tuple] = None):
        """
        Create a new FSPConfiguration.

        Channel averaging map is an optional list of 20 x (int,int) tuples.

        :param fsp_id: FSP configuration ID [1..27]
        :param function_mode: FSP function mode
        :param frequency_slice_id: frequency slicer ID [1..26]
        :param corr_bandwidth: correlator bandwidth [0..6]
        :param integration_time: integration time in ms
        :param channel_averaging_map: Optional channel averaging map
        """

        if not 1 <= fsp_id <= 27:
            raise ValueError('FSP ID must be in range 1..27. Got {}'.format(fsp_id))
        self.fsp_id = fsp_id

        self.function_mode = function_mode

        if not 1 <= frequency_slice_id <= 26:
            msg = ('Frequency slice ID must be in range 1..26. Got {}'
                   ''.format(frequency_slice_id))
            raise ValueError(msg)
        self.frequency_slice_id = frequency_slice_id

        if not 0 <= corr_bandwidth <= 6:
            msg = ('Correlator bandwidth must be in range 0..6. Got {}'.format(corr_bandwidth))
            raise ValueError(msg)
        self.corr_bandwidth = corr_bandwidth

        if integration_time % 140:
            msg = ('Integration time must be a multiple of 140. Got {}'
                   .format(integration_time))
            raise ValueError(msg)
        if not 1 <= (integration_time / 140) <= 10:
            msg = ('Integration time must in range 1..10 * 140. Got {}'
                   ''.format(integration_time))
            raise ValueError(msg)
        self.integration_time = integration_time

        if channel_averaging_map and len(channel_averaging_map) != 20:
            msg = ('Number of tuples in channel averaging map must be 20. Got {}'
                   .format(len(channel_averaging_map)))
            raise ValueError(msg)
        self.channel_averaging_map = channel_averaging_map

    def __eq__(self, other):
        if not isinstance(other, FSPConfiguration):
            return False
        return self.fsp_id == other.fsp_id \
               and self.function_mode == other.function_mode \
               and self.frequency_slice_id == other.frequency_slice_id \
               and self.corr_bandwidth == other.corr_bandwidth \
               and self.integration_time == other.integration_time \
               and self.channel_averaging_map == other.channel_averaging_map


class CSPConfiguration:
    """
    Class to hold all CSP configuration.
    """

    def __init__(self, scan_id: int, frequency_band: ReceiverBand,
                 fsp_configs: List[FSPConfiguration]):
        """
        Create a new CSPConfiguration.

        :param scan_id: the scan ID
        :param frequency_band: the frequency band to set
        :param fsp_configs: the FSP configurations to set
        """
        self.scan_id = scan_id
        self.frequency_band = frequency_band
        self.fsp_configs = fsp_configs

    def __eq__(self, other):
        if not isinstance(other, CSPConfiguration):
            return False
        return self.scan_id == other.scan_id \
               and self.frequency_band == other.frequency_band \
               and self.fsp_configs == other.fsp_configs

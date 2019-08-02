"""
The messages module provides simple Python representations of the structured
request and response for the TMC SubArrayNode.Configure command.
"""
from enum import Enum
from typing import Dict, List, Tuple

from astropy.coordinates import SkyCoord

__all__ = ['ConfigureRequest', 'DishConfiguration', 'PointingConfiguration', 'Target',
           'ReceiverBand', 'ProcessingBlockConfiguration', 'SDPParameters',
           'SDPScan', 'SDPScanParameters', 'SDPWorkflow', 'SDPConfiguration',
           'CSPConfiguration', 'FSPConfiguration', 'FSPFunctionMode']


class Target:
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that RA and Dec must be provided, hence
    non-ra/dec frames such as galactic are not supported.
    """
    OFFSET_MARGIN_IN_RAD = 6e-17  # Arbitrary small number

    #  pylint: disable=too-many-arguments
    def __init__(self, ra, dec, name='', frame='icrs', unit=('hourangle', 'deg')):
        self.coord = SkyCoord(ra, dec, unit=unit, frame=frame)
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Target):
            return False

        # Please replace this with a  more elegant way of dealing with differences
        # due to floating point arithmetic when comparing targets
        # defined in different ways.
        sep = self.coord.separation(other.coord)

        return self.name == other.name \
               and self.coord.frame.name == other.coord.frame.name \
               and sep.radian < self.OFFSET_MARGIN_IN_RAD

    def __repr__(self):
        raw_ra = self.coord.ra.value
        raw_dec = self.coord.dec.value
        units = (self.coord.ra.unit.name, self.coord.dec.unit.name)
        frame = self.coord.frame.name
        name = self.name
        return '<Target(ra={!r}, dec={!r}, name={!r}, frame={!r}, unit={!r})>'.format(
            raw_ra, raw_dec, name, frame, units
        )

    def __str__(self):
        frame = self.coord.frame.name
        name = self.name
        hmsdms = self.coord.to_string(style='hmsdms')
        return '<Target: {!r} ({} {})>'.format(name, hmsdms, frame)


class PointingConfiguration:  # pylint: disable=too-few-public-methods
    """
    PointingConfiguration specifies where the subarray receptors are going to
    point.
    """

    def __init__(self, target: Target):
        self.target = target

    def __eq__(self, other):
        if not isinstance(other, PointingConfiguration):
            return False
        return self.target == other.target


class ReceiverBand(Enum):
    """
    ReceiverBand is an enumeration of SKA MID receiver bands.
    """

    BAND_1 = '1'
    BAND_2 = '2'
    BAND_5A = '5a'
    BAND_5B = '5b'


class DishConfiguration:  # pylint: disable=too-few-public-methods
    """
    DishConfiguration specifies how SKA MID dishes in a sub-array should be
    configured. At the moment, this is limited to setting the receiver band.
    """

    def __init__(self, receiver_band: ReceiverBand):
        self.receiver_band = receiver_band

    def __eq__(self, other):
        if not isinstance(other, DishConfiguration):
            return False
        return self.receiver_band == other.receiver_band


class SDPWorkflow:  # pylint: disable=too-few-public-methods
    """
    Defines the SDP Workflow at the present we supply the parameters directly but
    once we understand more workflows this could be replaced with a lookup
    """

    def __init__(self, workflow_id: str, workflow_type: str, version: str):
        self.id = workflow_id  # pylint: disable=invalid-name
        self.type = workflow_type
        self.version = version

    def __eq__(self, other):
        if not isinstance(other, SDPWorkflow):
            return False
        return self.id == other.id \
               and self.type == other.type \
               and self.version == other.version


# pylint: disable=too-many-arguments
class SDPParameters:
    """
    Defines the key parameters for the SDPConfiguration
    """

    def __init__(self, num_stations: int, num_channels: int, num_polarisations: int,
                 freq_start_hz: float, freq_end_hz: float, target_fields: Dict[str, Target]):
        """
        :param num_stations: integer number of stations
        :param num_channels: integer number of channels
        :param num_polarisations: integer number of polarisations
        :param freq_start_hz: float start frequency in hz
        :param freq_end_hz: float end frequency in hz
        :param target_fields: Dict[str, Target]
        """
        self.num_stations = num_stations
        self.num_channels = num_channels
        self.num_polarisations = num_polarisations
        self.freq_start_hz = freq_start_hz
        self.freq_end_hz = freq_end_hz
        self.target_fields = target_fields

    def __eq__(self, other):
        if not isinstance(other, SDPParameters):
            return False
        return self.num_stations == other.num_stations \
               and self.num_channels == other.num_channels \
               and self.num_polarisations == other.num_polarisations \
               and self.freq_start_hz == other.freq_start_hz \
               and self.freq_end_hz == other.freq_end_hz \
               and self.target_fields == other.target_fields


class SDPScan:  # pylint: disable=too-few-public-methods
    """
    Block containing the SDPConfiguration for a single scan
    """

    def __init__(self, field_id: int, interval_ms: int):
        """
        :param field_id:
        :param interval_ms:
        """
        self.field_id = field_id
        self.interval_ms = interval_ms

    def __eq__(self, other):
        if not isinstance(other, SDPScan):
            return False
        return self.field_id == other.field_id \
               and self.interval_ms == other.interval_ms


class SDPScanParameters:  # pylint: disable=too-few-public-methods
    """
    SDPScans are indexed by a unique ID
    """

    def __init__(self, scan_parameters: Dict[str, SDPScan]):
        self.scan_parameters = scan_parameters

    def __eq__(self, other):
        if not isinstance(other, SDPScanParameters):
            return False
        return self.scan_parameters == other.scan_parameters


class ProcessingBlockConfiguration:  # pylint: disable=too-few-public-methods
    """
    ProcessingBlockConfiguration contains the complete configuration for a
    single single SDP Processing Block

    :param sb_id: The ID of the Scheduling Block
    :param sbi_id:  The ID of the Scheduling Block instance
    :param workflow: Structure representing the type of SDP workflow
    :param parameters: SDP configuration parameters for this particular
        configuration
    :param scan_parameters: Dictionary of the parameters for particular scans
        keyed by the scan ID
    """

    # pylint: disable=too-many-arguments
    def __init__(self, sb_id: str, sbi_id: str, workflow: SDPWorkflow,
                 parameters: SDPParameters, scan_parameters: Dict[str, SDPScan]):
        """
        :type sb_id: str
        :type sbi_id: str
        :type workflow: ska.cdm.messages.subarray_node.configure.SDPWorkflow
        :type parameters: ka.cdm.messages.subarray_node.configure.SDPParameters
        :type scan_parameters: Dict[str, ska.cdm.messages.subarray_node.configure.SDPScan]
        """
        self.sb_id = sb_id
        self.sbi_id = sbi_id
        self.workflow = workflow
        self.parameters = parameters
        self.scan_parameters = scan_parameters

    def __eq__(self, other):
        if not isinstance(other, ProcessingBlockConfiguration):
            return False
        return self.sb_id == other.sb_id \
               and self.sbi_id == other.sbi_id \
               and self.workflow == other.workflow \
               and self.parameters == other.parameters \
               and self.scan_parameters == other.scan_parameters


class SDPConfiguration:
    """
    SDPConfiguration is the envelope for the SDP processing block
    configuration, specified once per SB, and the SDP per-scan configuration,
    which is specified from the second scan onwards.
    """

    def __init__(self, configure: List[ProcessingBlockConfiguration] = None,
                 configure_scan: SDPScanParameters = None):
        self.configure = configure
        self.configure_scan = configure_scan

    def __eq__(self, other):
        if not isinstance(other, SDPConfiguration):
            return False
        return self.configure == other.configure \
               and self.configure_scan == other.configure_scan


class FSPFunctionMode(Enum):
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


class ConfigureRequest:  # pylint: disable=too-few-public-methods
    """
    ConfigureRequest encapsulates the arguments required for the TMC
    SubArrayNode.Configure() command.
    """

    def __init__(self, scan_id: int, pointing: PointingConfiguration = None,
                 dish: DishConfiguration = None, sdp: SDPConfiguration = None,
                 csp: CSPConfiguration = None):
        self.scan_id = scan_id
        self.pointing = pointing
        self.dish = dish
        self.sdp = sdp
        self.csp = csp

    def __eq__(self, other):
        if not isinstance(other, ConfigureRequest):
            return False
        return self.scan_id == other.scan_id \
               and self.pointing == other.pointing \
               and self.dish == other.dish \
               and self.sdp == other.sdp \
               and self.csp == other.csp

"""
The messages module provides simple Python representations of the structured
request and response for the TMC SubArrayNode.Configure command.
"""
from enum import Enum
from typing import Dict, Union

from astropy.coordinates import SkyCoord

__all__ = ['ConfigureRequest', 'DishConfiguration', 'PointingConfiguration', 'Target',
           'ReceiverBand', 'SDPConfigurationBlock', 'SDPConfigureScan', 'SDPParameters',
           'SDPScan', 'SDPScanParameters', 'SDPConfigure', 'SDPWorkflow']


class Target:  # pylint: disable=too-few-public-methods  # pylint: disable=too-many-arguments
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that RA and Dec must be provided, hence
    non-ra/dec frames such as galactic are not supported.
    """
    OFFSET_MARGIN_IN_RAD = 6e-17  # Arbitrary small number

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
        same_position = (sep.radian < self.OFFSET_MARGIN_IN_RAD)

        result = [self.name == other.name,
                  same_position,
                  self.coord.frame.name == other.coord.frame.name]
        return all(result)

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


class ReceiverBand(Enum):  # pylint: disable=too-few-public-methods
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

    def __init__(self, wf_id: str, wf_type: str, version: str):
        self.wf_id = wf_id
        self.wf_type = wf_type
        self.version = version

    def __eq__(self, other):
        if not isinstance(other, SDPWorkflow):
            return False
        results = [self.wf_id == other.wf_id,
                   self.wf_type == other.wf_type,
                   self.version == other.version]
        return all(results)

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
class SDPParameters:
    """
    Defines the key parameters for the SDPConfiguration
    """

    def __init__(self, num_stations: int, num_chanels: int, num_polarisations: int,
                 freq_start_hz: float, freq_end_hz: float, target_fields: Dict[str, Target]):
        """
        :param num_stations: integer number of stations
        :param num_chanels: integer number of channels
        :param num_polarisations: integer number of polarisations
        :param freq_start_hz: float start frequency in hz
        :param freq_end_hz: float end frequency in hz
        :param target_fields: Dict[str, Target]
        """
        self.num_stations = num_stations
        self.num_chanels = num_chanels
        self.num_polarisations = num_polarisations
        self.freq_start_hz = freq_start_hz
        self.freq_end_hz = freq_end_hz
        self.target_fields = target_fields

    def __eq__(self, other):
        if not isinstance(other, SDPParameters):
            return False
        results = [self.num_stations == other.num_stations,
                   self.num_chanels == other.num_chanels,
                   self.num_polarisations == other.num_polarisations,
                   self.freq_start_hz == other.freq_start_hz,
                   self.freq_end_hz == other.freq_end_hz,
                   self.target_fields == other.target_fields]
        return all(results)


class SDPScan:  # pylint: disable=too-few-public-methods
    """
    Block containing the SDPConfiguration for a single scan
    """

    def __init__(self, field_id: int, interval_ms: int) -> None:
        """
        :param field_id:
        :param interval_ms:
        """
        self.field_id = field_id
        self.interval_ms = interval_ms

    def __eq__(self, other):
        if not isinstance(other, SDPScan):
            return False
        return all([self.field_id == other.field_id,
                    self.interval_ms == other.interval_ms])


class SDPScanParameters:  # pylint: disable=too-few-public-methods
    """SDPScans are indexed by a unique ID"""
    def __init__(self, scan_parameters: Dict[str, SDPScan]):
        self.scan_parameters = scan_parameters

    def __eq__(self, other):
        if not isinstance(other, SDPScanParameters):
            return False
        return self.scan_parameters == other.scan_parameters


class SDPConfigurationBlock:  # pylint: disable=too-few-public-methods
    """
    Block containing the complete SDPConfiguration for a single SDP Processing Block

    :param sb_id: The ID of the Scheduling Block
    :param sbi_id:  The ID of the Scheduling Block instance
    :param workflow: Structure representing the type of SDP workflow
    :param parameters: SDP configuration parameters for this particular configuration
    :param scan_parameters: Dictionary of the parameters for particular scans keyed by the scan ID
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
        if not isinstance(other, SDPConfigurationBlock):
            return False
        results = [self.sb_id == other.sb_id,
                   self.sbi_id == other.sbi_id,
                   self.workflow == other.workflow,
                   self.parameters == other.parameters,
                   self.scan_parameters == other.scan_parameters]

        return all(results)


class SDPConfigure:  # pylint: disable=too-few-public-methods
    """
    SDPConfigure encapsulates the arguments required for the SDP for
    the SubArrayNode.Configure() command for the initial request for each SB
    """

    def __init__(self, configure: [SDPConfigurationBlock]):
        self.configure = configure

    def __eq__(self, other):
        if not isinstance(other, SDPConfigure):
            return False
        return self.configure == other.configure


class SDPConfigureScan:  # pylint: disable=too-few-public-methods
    """
    SDPConfigureScan encapsulates the arguments required for the SDP for
    the SubArrayNode.Configure() command for each scan after the first
    """

    def __init__(self, configure_scan: SDPScanParameters):
        self.configure_scan = configure_scan

    def __eq__(self, other):
        if not isinstance(other, SDPConfigureScan):
            return False
        return self.configure_scan == other.configure_scan


class ConfigureRequest:  # pylint: disable=too-few-public-methods
    """
    ConfigureRequest encapsulates the arguments required for the TMC
    SubArrayNode.Configure() command.
    """

    def __init__(self, scan_id: int, pointing: PointingConfiguration,
                 dish: DishConfiguration, sdp: Union[SDPConfigure, SDPConfigureScan]):
        self.scan_id = scan_id
        self.pointing = pointing
        self.dish = dish
        self.sdp = sdp

    def __eq__(self, other):
        if not isinstance(other, ConfigureRequest):
            return False
        result = [
            self.pointing == other.pointing,
            self.dish == other.dish,
            self.scan_id == other.scan_id,
            self.sdp == other.sdp
        ]

        return all(result)

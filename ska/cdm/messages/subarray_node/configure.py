"""
The messages module provides simple Python representations of the structured
request and response for the TMC SubArrayNode.Configure command.
"""
from enum import Enum
from typing import Dict

from astropy.coordinates import SkyCoord

__all__ = ['ConfigureRequest', 'DishConfiguration', 'PointingConfiguration', 'Target',
           'ReceiverBand', 'SDPConfigurationBlock', 'SDPConfigureScan', 'SDPParameters',
           'SDPScan', 'SDPConfigure', 'SDPWorkflow']

class Target:
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that RA and Dec must be provided, hence
    non-ra/dec frames such as galactic are not supported.
    """
    def __init__(self, ra, dec, name='', frame='icrs', unit=('hourangle', 'deg')):
        self.coord = SkyCoord(ra, dec, unit=unit, frame=frame)
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Target):
            return False
        # As the target frame is ra/dec, we can rely on .ra and .dec
        # properties to be present
        return all([self.name == other.name,
                    self.coord.ra == other.coord.ra,
                    self.coord.dec == other.coord.dec,
                    self.coord.frame.name == other.coord.frame.name])

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


class ConfigureRequest:  # pylint: disable=too-few-public-methods
    """
    ConfigureRequest encapsulates the arguments required for the TMC
    SubArrayNode.Configure() command.
    """

    def __init__(self, scan_id: int, pointing: PointingConfiguration, dish: DishConfiguration):
        self.scan_id = scan_id
        self.pointing = pointing
        self.dish = dish

    def __eq__(self, other):
        if not isinstance(other, ConfigureRequest):
            return False
        return self.pointing == other.pointing \
               and self.dish == other.dish \
               and self.scan_id == other.scan_id


class SDPWorkflow:

    def __init__(self, wf_id: str, wf_type: str, version: str):
        self.wf_id = wf_id
        self.wf_type = wf_type
        self.version = version

    def __eq__(self, other):
        if not isinstance(other, SDPWorkflow):
            return False
        return all([self.wf_id == other.wf_id,
                    self.wf_type == other.wf_type,
                    self.version == other.version])


class SDPParameters:

    def __init__(self, num_stations: int, num_chanels: int, num_polarisations: int, freq_start_hz: float,
                 freq_end_hz: float, target_fields: Dict[int, Target]):
        self.num_stations = num_stations
        self.num_chanels = num_chanels
        self.num_polarisations = num_polarisations
        self.freq_start_hz = freq_start_hz
        self.freq_end_hz = freq_end_hz
        self.target_fields = target_fields

    def __eq__(self, other):
        if not isinstance(other, SDPParameters):
            return False
        return all([self.num_stations == other.num_stations,
                    self.num_chanels == other.num_chanels,
                    self.num_polarisations == other.num_polarisations,
                    self.freq_start_hz == other.freq_start_hz,
                    self.freq_end_hz == other.freq_end_hz,
                    self.target_fields == other.target_fields])


class SDPScan:
    def __init__(self, field_id: int, interval_ms: int) -> None:
        self.field_id = field_id
        self.interval_ms = interval_ms

    def __eq__(self, other):
        if not isinstance(other, SDPScan):
            return False
        return all([self.field_id == other.field_id,
                    self.interval_ms == other.interval_ms])


class SDPScanParameters:

    def __init__(self, scan_parameters: Dict[str, SDPScan]):
        self.scan_parameters = scan_parameters

    def __eq__(self, other):
        if not isinstance(other, SDPScanParameters):
            return False
        return self.scan_parameters == other.scan_parameters


class SDPConfigurationBlock:

    def __init__(self, sb_id: str, sbi_id: str, workflow: SDPWorkflow,
                 parameters: SDPParameters, scan_parameters: Dict[str, SDPScan]):
        """

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
        return all([self.sb_id == other.sb_id,
                    self.sbi_id == other.sbi_id,
                    self.workflow == other.workflow,
                    self.parameters == other.parameters,
                    self.scan_parameters == other.scan_parameters])


class SDPConfigure:

    def __init__(self, configure: [SDPConfigurationBlock]):
        self.configure = configure

    def __eq__(self, other):
        if not isinstance(other, SDPConfigure):
            return False
        return self.configure == other.configure


class SDPConfigureScan:

    def __init__(self, configure_scan: SDPScanParameters):
        self.configure_scan = configure_scan

    def __eq__(self, other):
        if not isinstance(other, SDPConfigureScan):
            return False
        return self.configure_scan == other.configure_scan


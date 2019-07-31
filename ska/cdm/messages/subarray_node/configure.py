"""
The messages module provides simple Python representations of the structured
request and response for the TMC SubArrayNode.Configure command.
"""
from enum import Enum
from typing import List, Tuple

from astropy.coordinates import SkyCoord

__all__ = ['ConfigureRequest', 'DishConfiguration', 'PointingConfiguration', 'Target',
           'ReceiverBand', 'CSPConfiguration', 'FSPConfiguration', 'FSPFunctionMode']


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
    FSPConfiguration class holds the fsp details for CSP configuration in below format
    "fspID": "1",
    "functionMode": "CORR",  // Set FSP to correlation mode
    "frequencySliceID": 1,   // Tell FSP to process frequency slice #1
    "integrationTime": 1400  // Set FSP to 1400ms integration time.
    "corrBandwidth": 0       // Correlate the entire frequency slice
    "channelAveragingMap": [
          (1,2), (745,0), (1489,0), (2233,0), (2977,0), (3721,0), (4465,0),
          (5209,0), (5953,0), (6697,0), (7441,0), (8185,0), (8929,0), (9673,0),
          (10417,0), (11161,0), (11905,0), (12649,0), (13393,0), (14137,0)
    //Table 20 x 2 integers. Each of 20 entries contains:Channel ID, Averaging factor. Each FSP produces 14880

    """

    def __init__(self, fsp_id: int, function_mode: FSPFunctionMode, frequency_slice_id: int,
                 integration_time: int, corr_bandwidth: int, channel_averaging_map: List[Tuple] = None):
        """

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
            raise ValueError('Frequency slice ID must be in range 1..26. Got {}'.format(frequency_slice_id))
        self.frequency_slice_id = frequency_slice_id

        if not 0 <= corr_bandwidth <= 6:
            raise ValueError('Correlator bandwidth must be in range 0..6. Got {}'.format(corr_bandwidth))
        self.corr_bandwidth = corr_bandwidth

        if integration_time % 140:
            raise ValueError('Integration time must be a multiple of 140. Got {}'.format(integration_time))
        if not 1 <= (integration_time / 140) <= 10:
            raise ValueError('Integration time must in range 1..10 * 140. Got {}'.format(integration_time))
        self.integration_time = integration_time

        if len(channel_averaging_map) < 20  or len(channel_averaging_map) >20 :
            raise ValueError('Number of tuples in chanel averaging map must be 20. Got {}'.format(len(channel_averaging_map)))
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
    Encapsulating class to hold CSP configuration
    """

    def __init__(self, scan_id: int, frequency_band: ReceiverBand, fsp_configs: List[FSPConfiguration]):
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

    def __init__(self, scan_id: int, pointing: PointingConfiguration, dish: DishConfiguration, csp: CSPConfiguration):
        self.scan_id = scan_id
        self.pointing = pointing
        self.dish = dish
        self.csp = csp

    def __eq__(self, other):
        if not isinstance(other, ConfigureRequest):
            return False
        return self.scan_id == other.scan_id \
               and self.pointing == other.pointing \
               and self.dish == other.dish \
               and self.csp == other.csp

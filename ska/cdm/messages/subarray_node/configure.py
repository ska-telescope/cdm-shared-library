"""
The messages module provides simple Python representations of the structured
request and response for the TMC SubArrayNode.Configure command.
"""
from enum import Enum

from astropy.coordinates import SkyCoord

__all__ = ['ConfigureRequest', 'DishConfiguration', 'PointingConfiguration', 'Target',
           'ReceiverBand', 'CSPConfiguration', 'FSPConfiguration']


class Target:
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that RA and Dec must be provided, hence
    non-ra/dec frames such as galactic are not supported.
    """

    def __init__(self, ra, dec, name='', frame='icrs', unit='rad'):
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

    def __str__(self):
        units = self.coord.ra.unit.name
        frame = self.coord.frame.name
        name = self.name
        # named ra_val rather than ra to satisfy static analysis
        ra_val = self.coord.ra.value
        dec_val = self.coord.dec.value
        return '<Target(ra={}, dec={}, name={!r}, frame={!r}, unit={!r})>'.format(
            ra_val, dec_val, name, frame, units
        )


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


class FSPConfiguration:
    """

    FSPConfiguration class holds the fsp details for CSP configuration
    fspID": "1",
        "functionMode": "CORR",  // Set FSP to correlation mode
        // Since receptors are not given, FSP uses all receptors assigned to the
        // subarray
        "frequencySliceID": 1,   // Tell FSP to process frequency slice #1
        "integrationTime": 1400  // Set FSP to 1400ms integration time.
        "corrBandwidth": 0       // Correlate the entire frequency slice
        //
        // Send the minimum possible number of channels to SDP by averaging
        // the first 744 fine channels down to 372 channels (=744/2). Do not
        // send any other fine channel groups to SDP (=<chan ID>,0).
        //
        "channelAveragingMap": [
          (1,2), (745,0), (1489,0), (2233,0), (2977,0), (3721,0), (4465,0),
          (5209,0), (5953,0), (6697,0), (7441,0), (8185,0), (8929,0), (9673,0),
          (10417,0), (11161,0), (11905,0), (12649,0), (13393,0), (14137,0)
    """
    def __init__(self,fspID: str, function_mode:str, frequency_slice_ID, integration_time, corr_bandwidth, channel_averaging_map):
        self.fsp_ID =  fspID
        self.function_mode = function_mode
        self.frequency_slice_ID = frequency_slice_ID
        self.integration_time = integration_time,
        self.corr_bandwidth = corr_bandwidth
        self.channel_averaging_map = channel_averaging_map


class CSPConfiguration:
    """
    Encapsulating class to hold CSP configuration
    """
    def __init__(self, frequency_band: str, fsp:FSPConfiguration):
        self.frequency_band = frequency_band
        self.fsp = fsp


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
        return self.pointing == other.pointing and self.dish == other.dish and self.scan_id == other.scan_id and self.csp == other.csp

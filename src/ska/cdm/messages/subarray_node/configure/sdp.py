"""
The configure.sdp module contains Python classes that represent the various
aspects of SDP configuration that may be specified in a SubArrayNode.configure
command.
"""
from typing import Dict, List

from .core import Target

__all__ = ['ProcessingBlockConfiguration', 'SDPParameters', 'SDPScan', 'SDPScanParameters',
           'SDPWorkflow', 'SDPConfiguration', 'NewSDPConfiguration', 'NewProcessingBlockConfiguration',
           'PbDependency', 'NewSDPParameters', 'ScanType', 'SubBand']


class SDPWorkflow:  # pylint: disable=too-few-public-methods
    """
    Defines the SDP Workflow at the present we supply the parameters directly but
    once we understand more workflows this could be replaced with a lookup
    """

    def __init__(self, workflow_id: str, workflow_type: str, version: str):
        self.workflow_id = workflow_id
        self.workflow_type = workflow_type
        self.version = version

    def __eq__(self, other):
        if not isinstance(other, SDPWorkflow):
            return False
        return self.workflow_id == other.workflow_id \
               and self.workflow_type == other.workflow_type \
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


class SubBand:
    """
    Represents ...
    """
    def __init__(self, freq_min: float, freq_max: float, nchan: int, input_link_map: List[List]):
        self.freq_min = freq_min
        self.freq_max = freq_max
        self.nchan = nchan
        self.input_link_map = input_link_map
    
    def __eq__(self, other):
        if not isinstance(other, SubBand):
            return False
        return self.freq_min == other.freq_min \
               and self.freq_max == other.freq_max \
               and self.nchan == other.nchan \
               and self.input_link_map == other.input_link_map


class ScanType:
    """
    Represents ...
    """
    def __init__(self, st_id, coordinate_system: str, ra: str, dec: str, sub_bands: List[SubBand]):
        self.st_id = st_id
        self.coordinate_system = coordinate_system
        self.ra = ra
        self.dec = dec
        self.sub_bands = sub_bands

    def __eq__(self, other):
        if not isinstance(other, ScanType):
            return False
        return self.st_id == other.st_id \
               and self.coordinate_system == other.coordinate_system \
               and self.ra == other.ra \
               and self.dec == other.dec \
               and self.sub_bands == other.sub_bands
               

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


class NewSDPParameters:
    """
    Represents ...
    """
    def __eq__(self, other):
        if not isinstance(other, NewSDPParameters):
            return False
        return True


class PbDependency:
    """
    Represents ...
    """

    def __init__(self, pb_id: str, pb_type: List[str]):
        self.pb_id = pb_id
        self.pb_type = pb_type

    def __eq__(self, other):
        if not isinstance(other, PbDependency):
            return False
        return self.pb_id == other.pb_id \
               and self.pb_type == other.pb_type


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


class NewProcessingBlockConfiguration(ProcessingBlockConfiguration):
    """
    Represents ...
    """
    def __init__(self, pb_id: str, workflow: SDPWorkflow, parameters: NewSDPParameters,
                 dependencies: List[PbDependency] = None):
        self.pb_id = pb_id
        self.workflow = workflow
        self.parameters = parameters
        self.dependencies = dependencies

    def __eq__(self, other):
        if not isinstance(other, NewProcessingBlockConfiguration):
            return False
        return self.pb_id == other.pb_id \
               and self.workflow == other.workflow \
               and self.parameters == other.parameters \
               and self.dependencies == other.dependencies


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


class NewSDPConfiguration(SDPConfiguration):
    """
    Represents ...
    """
    def __init__(self, sdp_id: str, max_length: float, scan_types: List[ScanType], processing_blocks: List[NewProcessingBlockConfiguration]):
        self.sdp_id = sdp_id
        self.max_length = max_length
        self.scan_types = scan_types
        self.processing_blocks = processing_blocks

    def __eq__(self, other):
        if not isinstance(other, SDPConfiguration):
            return False
        return self.sdp_id == other.sdp_id \
               and self.max_length == other.max_length \
               and self.scan_types == other.scan_types \
               and self.processing_blocks == other.processing_blocks

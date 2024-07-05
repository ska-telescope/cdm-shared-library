"""
The configure.csp module contains Python classes that represent the various
aspects of CSP configuration that may be specified in a SubArrayNode.configure
command.
"""
from enum import Enum
from typing import List, Optional, Tuple

from pydantic import AliasChoices, Field

from ska_tmc_cdm.messages.base import CdmObject

from . import core

__all__ = [
    "CSPConfiguration",
    "FSPConfiguration",
    "FSPFunctionMode",
    "CBFConfiguration",
    "SubarrayConfiguration",
    "CommonConfiguration",
    "LowCBFConfiguration",
    "StationConfiguration",
    "StnBeamConfiguration",
    "VisFspConfiguration",
    "VisConfiguration",
]


class FSPFunctionMode(Enum):
    """
    FSPFunctionMode is an enumeration of the available FSP modes.
    """

    CORR = "CORR"
    PSS_BF = "PSS-BF"
    PST_BF = "PST-BF"
    VLBI = "VLBI"


class FSPConfiguration(CdmObject):
    """
    FSPConfiguration defines the configuration for a CSP Frequency Slice
    Processor.

    Channel averaging map is an optional list of 20 x (int,int) tuples.

    :param fsp_id: FSP configuration ID [1..27]
    :param function_mode: FSP function mode
    :param frequency_slice_id: frequency slicer ID [1..26]
    :param zoom_factor: zoom factor [0..6]
    :param integration_factor: integration factor [1..10]
    :param channel_averaging_map: Optional channel averaging map
    :param output_link_map: Optional output link map
    :param channel_offset: Optional FSP channel offset
    :param zoom_window_tuning: Optional zoom window tuning

    :raises ValueError: Invalid parameter values entered
    """

    fsp_id: int = Field(ge=1, le=27)  # 1 <= id <= 27
    function_mode: FSPFunctionMode = Field()
    frequency_slice_id: int = Field(ge=1, le=26)
    integration_factor: int = Field(ge=1, le=10)
    zoom_factor: int = Field(ge=0, le=6)
    # FIXME: should be Field(default_factory=list, max_length=20)?
    channel_averaging_map: Optional[List[Tuple]] = Field(None, max_length=20)
    # could we add enforcements for output_link_map? What are the limits?
    output_link_map: Optional[
        List[Tuple]
    ] = None  # FIXME: Field(default_factory=list)?
    channel_offset: Optional[int] = None
    zoom_window_tuning: Optional[int] = None


class SubarrayConfiguration(CdmObject):
    """
    Class to hold the parameters relevant only for the current sub-array device.

    :param sub-array_name: Name of the sub-array
    """

    subarray_name: Optional[str] = ""


class CommonConfiguration(CdmObject):
    """
    Class to hold the CSP sub-elements.

    :param config_id: CSP configuration ID
    :param frequency_band: the frequency band to set
    :param subarray_id: an ID of sub-array device
    :param band_5_tuning: band 5 receiver to set (optional)
    """

    config_id: Optional[str] = ""
    frequency_band: Optional[core.ReceiverBand] = None
    subarray_id: Optional[int] = None
    band_5_tuning: Optional[List[float]] = None


class StnBeamConfiguration(CdmObject):
    """
    Class to hold Stations Beam Configuration.

    :param stn_beam_id: stn_beam_id
    :param beam_id: beam_id
    :param freq_ids: freq_ids
    :param delay_poly: delay_poly
    """

    beam_id: Optional[int]
    freq_ids: List[int]
    stn_beam_id: Optional[int] = None
    delay_poly: Optional[str] = None


class VisStnBeamConfiguration(CdmObject):
    """
    Class to hold Vis Stations Beam Configuration.

    :param stn_beam_id: stn_beam_id
    :param host: host
    :param port: port
    :param mac: mac
    :param integration_ms: integration_ms
    """

    stn_beam_id: Optional[int]
    integration_ms: int
    host: Optional[List[Tuple[int, str]]] = None
    port: Optional[List[Tuple[int, int, int]]] = None
    mac: Optional[List[Tuple[int, str]]] = None


class StationConfiguration(CdmObject):
    """
    Class to hold Stations Configuration.

    :param stns: stns
    :param stn_beams: stn_beams
    """

    stns: Optional[List[List[int]]] = None
    stn_beams: Optional[List[StnBeamConfiguration]] = None


class VisFspConfiguration(CdmObject):
    """
    Class to hold Visibility(Vis) Configuration.

    :param function_mode: function_mode
    :param fsp_ids: fsp_ids
    :param firmware: firmware
    """

    function_mode: Optional[str] = None
    fsp_ids: Optional[List[int]] = None
    firmware: Optional[str] = None


class VisConfiguration(CdmObject):
    """
        Class to hold Vis Configuration.
    firmware
        :param fsp: fsp
        :param stn_beams: stn_beams
    """

    fsp: Optional[VisFspConfiguration] = None
    stn_beams: Optional[List[VisStnBeamConfiguration]] = None


class LowCBFConfiguration(CdmObject):
    """
    Class to hold Low CBF Configuration.

    :param stations: stations
    :param vis: vis
    """

    stations: Optional[StationConfiguration] = None
    vis: Optional[VisConfiguration] = None


class VLBIConfiguration(CdmObject):
    pass


class CBFConfiguration(CdmObject):
    """
    Class to hold all FSP and VLBI configurations.

    :param fsp_configs: the FSP configurations to set
    :param vlbi_config: the VLBI configurations to set, it is optional
    """

    fsp_configs: List[FSPConfiguration] = Field(
        serialization_alias="fsp",
        validation_alias=AliasChoices("fsp", "fsp_configs"),
    )
    # TODO: In future when csp Interface 2.2 will be used than type of vlbi_config parameter
    #  will be replaced with the respective class(VLBIConfiguration)
    vlbi_config: Optional[dict] = Field(
        default=None,
        serialization_alias="vlbi",
        validation_alias=AliasChoices("vlbi", "vlbi_config"),
    )


class PSTConfiguration(CdmObject):
    pass


class PSSConfiguration(CdmObject):
    pass


class CSPConfiguration(CdmObject):
    """
    Class to hold all CSP configuration. In order to support backward
    compatibility, We have kept old attributes as it is and added
    support of new attributes as per ADR-18

    :param interface: url string to determine JsonSchema version
    :param subarray: Sub-array configuration to set
    :param common: the common CSP elemenets to set
    :param cbf_config: the CBF configurations to set
    :param pst_config: the PST configurations to set
    :param pss_config: the PSS configurations to set
    """

    interface: Optional[str] = None
    subarray: Optional[SubarrayConfiguration] = None
    common: Optional[CommonConfiguration] = None
    cbf_config: Optional[CBFConfiguration] = Field(
        default=None,
        serialization_alias="midcbf",
        validation_alias=AliasChoices("midcbf", "cbf_config"),
    )
    # TODO: In the future when csp Interface 2.2 is adopted, pst_config and pss_config
    # should not accept dict types as inputs.
    pst_config: Optional[PSTConfiguration | dict] = Field(
        default=None,
        serialization_alias="pst",
        validation_alias=AliasChoices("pst", "pst_config"),
    )
    pss_config: Optional[PSSConfiguration | dict] = Field(
        default=None,
        serialization_alias="pss",
        validation_alias=AliasChoices("pss", "pss_config"),
    )
    lowcbf: Optional[LowCBFConfiguration] = None

from typing import List, Tuple

from ska_tmc_cdm.messages.subarray_node.configure import core
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    LowCBFConfiguration,
    PSSConfiguration,
    PSTConfiguration,
    StationConfiguration,
    StnBeamConfiguration,
    SubarrayConfiguration,
    VisConfiguration,
    VisFspConfiguration,
)


class FSPConfigurationBuilder:
    """
    FSPConfigurationBuilder is a test data builder for FSPConfiguration objects.
    """

    def __init__(self):
        self.fsp_id = None
        self.function_mode = None
        self.frequency_slice_id = None
        self.integration_factor = None
        self.zoom_factor = None
        self.channel_averaging_map = None
        self.output_link_map = None
        self.channel_offset = None
        self.zoom_window_tuning = None

    def set_fsp_id(self, fsp_id: int) -> "FSPConfigurationBuilder":
        """
        Set the FSP configuration ID.
        :param fsp_id: Integer representing the FSP configuration ID.
        :raises ValueError: If the fsp_id is not within the range 1 to 27.
        """
        if not 1 <= fsp_id <= 27:
            raise ValueError("fsp_id must be between 1 and 27")
        self.fsp_id = fsp_id
        return self

    def set_function_mode(
        self, function_mode: FSPFunctionMode
    ) -> "FSPConfigurationBuilder":
        """
        Set the FSP function mode.
        :param function_mode: An instance of FSPFunctionMode enum.
        """
        self.function_mode = function_mode
        return self

    def set_frequency_slice_id(
        self, frequency_slice_id: int
    ) -> "FSPConfigurationBuilder":
        """
        Set the frequency slice ID.
        :param frequency_slice_id: Integer representing the frequency slice ID.
        :raises ValueError: If the frequency_slice_id is not within the range 1 to 26.
        """
        if not 1 <= frequency_slice_id <= 26:
            raise ValueError("frequency_slice_id must be between 1 and 26")
        self.frequency_slice_id = frequency_slice_id
        return self

    def set_integration_factor(
        self, integration_factor: int
    ) -> "FSPConfigurationBuilder":
        """
        Set the integration factor.
        :param integration_factor: Integer representing the integration factor.
        :raises ValueError: If the integration_factor is not within the range 1 to 10.
        """
        if not 1 <= integration_factor <= 10:
            raise ValueError("integration_factor must be between 1 and 10")
        self.integration_factor = integration_factor
        return self

    def set_zoom_factor(self, zoom_factor: int) -> "FSPConfigurationBuilder":
        """
        Set the zoom factor.
        :param zoom_factor: Integer representing the zoom factor.
        :raises ValueError: If the zoom_factor is not within the range 0 to 6.
        """
        if not 0 <= zoom_factor <= 6:
            raise ValueError("zoom_factor must be between 0 and 6")
        self.zoom_factor = zoom_factor
        return self

    def set_channel_averaging_map(
        self, channel_averaging_map: List[Tuple[int, int]]
    ) -> "FSPConfigurationBuilder":
        """
        Set the channel averaging map.
        :param channel_averaging_map: List of tuples representing the channel averaging map.
        """
        self.channel_averaging_map = channel_averaging_map
        return self

    def set_output_link_map(
        self, output_link_map: List[Tuple[int, int, int]]
    ) -> "FSPConfigurationBuilder":
        """
        Set the output link map.
        :param output_link_map: List of tuples representing the output link map.
        """
        self.output_link_map = output_link_map
        return self

    def set_channel_offset(self, channel_offset: int) -> "FSPConfigurationBuilder":
        """
        Set the channel offset.
        :param channel_offset: Integer representing the channel offset.
        """
        self.channel_offset = channel_offset
        return self

    def set_zoom_window_tuning(
        self, zoom_window_tuning: int
    ) -> "FSPConfigurationBuilder":
        """
        Set the zoom window tuning.
        :param zoom_window_tuning: Integer representing the zoom window tuning.
        """
        self.zoom_window_tuning = zoom_window_tuning
        return self

    def build(self) -> FSPConfiguration:
        """
        Builds or creates an instance of FSPConfiguration
        :return: An instance of FSPConfiguration with the specified configurations.
        """
        return FSPConfiguration(
            fsp_id=self.fsp_id,
            function_mode=self.function_mode,
            frequency_slice_id=self.frequency_slice_id,
            integration_factor=self.integration_factor,
            zoom_factor=self.zoom_factor,
            channel_averaging_map=self.channel_averaging_map,
            output_link_map=self.output_link_map,
            channel_offset=self.channel_offset,
            zoom_window_tuning=self.zoom_window_tuning,
        )


class SubarrayConfigurationBuilder:
    """
    SubarrayConfigurationBuilder is a test data builder for SubarrayConfiguration objects.
    """

    def __init__(self):
        self.subarray_name = None

    def set_subarray_name(self, subarray_name: str) -> "SubarrayConfigurationBuilder":
        """
        Set the name of the sub-array.

        :param subarray_name: String representing the name of the sub-array.
        :return: An instance of SubarrayConfigurationBuilder with the updated sub-array name.
        """
        self.subarray_name = subarray_name
        return self

    def build(self) -> SubarrayConfiguration:
        """
        Builds or creates an instance of SubarrayConfiguration with the set properties.
        :return: An instance of SubarrayConfiguration with the specified name.
        """
        return SubarrayConfiguration(subarray_name=self.subarray_name)


class CommonConfigurationBuilder:
    """
    CommonConfigurationBuilder is a test data builder for CommonConfiguration objects.
    """

    def __init__(self):
        self.config_id = None
        self.frequency_band = None
        self.subarray_id = None
        self.band_5_tuning = None

    def set_config_id(self, config_id: str) -> "CommonConfigurationBuilder":
        """
        Set the configuration ID.

        :param config_id: String representing the configuration ID.
        :return: An instance of CommonConfigurationBuilder with the updated configuration ID.
        """
        self.config_id = config_id
        return self

    def set_frequency_band(
        self, frequency_band: core.ReceiverBand
    ) -> "CommonConfigurationBuilder":
        """
        Set the frequency band.

        :param frequency_band: ReceiverBand instance representing the frequency band.
        :return: An instance of CommonConfigurationBuilder with the updated frequency band.
        """
        self.frequency_band = frequency_band
        return self

    def set_subarray_id(self, subarray_id: int) -> "CommonConfigurationBuilder":
        """
        Set the sub-array ID.

        :param subarray_id: Integer representing the sub-array ID.
        :return: An instance of CommonConfigurationBuilder with the updated sub-array ID.
        """
        self.subarray_id = subarray_id
        return self

    def set_band_5_tuning(
        self, band_5_tuning: List[float]
    ) -> "CommonConfigurationBuilder":
        """
        Set the band 5 tuning.

        :param band_5_tuning: List of floats representing the band 5 tuning.
        :return: An instance of CommonConfigurationBuilder with the updated band 5 tuning.
        """
        self.band_5_tuning = band_5_tuning
        return self

    def build(self) -> CommonConfiguration:
        """
        Builds or creates an instance of CommonConfiguration with the set properties.
        :return: An instance of CommonConfiguration with the specified configurations.
        """
        return CommonConfiguration(
            config_id=self.config_id,
            frequency_band=self.frequency_band,
            subarray_id=self.subarray_id,
            band_5_tuning=self.band_5_tuning,
        )


class CBFConfigurationBuilder:
    """
    CBFConfigurationBuilder is a test data builder for CBFConfiguration objects.
    """

    def __init__(self):
        self.fsp_configs = None
        self.vlbi_config = None

    def set_fsp_config(
        self, fsp_configs: List[FSPConfiguration]
    ) -> "CBFConfigurationBuilder":
        """
         Set Frequency Slice Processor (FSP) configuration.

        :param fsp_configs: List of FSPConfiguration instance to add to the CBF configuration.
        :return: An instance of CBFConfigurationBuilder with the added FSP configuration.
        """
        self.fsp_configs = fsp_configs
        return self

    def set_vlbi_config(self, vlbi_config: dict) -> "CBFConfigurationBuilder":
        """
        Set the VLBI configuration.

        :param vlbi_config: A dictionary representing the VLBI configuration.
        :return: An instance of CBFConfigurationBuilder with the updated VLBI configuration.
        """
        self.vlbi_config = vlbi_config
        return self

    def build(self) -> CBFConfiguration:
        """
        Builds or creates an instance of CBFConfiguration with the set properties.
        :return: An instance of CBFConfiguration with the specified configurations.
        """
        return CBFConfiguration(
            fsp_configs=self.fsp_configs, vlbi_config=self.vlbi_config
        )


class LowCBFConfigurationBuilder:
    """
    LowCBFConfigurationBuilder is a test data builder for LowCBFConfiguration objects.
    """

    def __init__(self):
        self.stations = None
        self.vis = None

    def set_stations(
        self, stations: StationConfiguration
    ) -> "LowCBFConfigurationBuilder":
        """
        Set the station configuration for the LowCBF.

        :param stations: A StationConfiguration instance representing the station configuration.
        :return: An instance of LowCBFConfigurationBuilder with the set station configuration.
        """
        self.stations = stations
        return self

    def set_vis(self, vis: VisConfiguration) -> "LowCBFConfigurationBuilder":
        """
        Set the visibility configuration for the LowCBF.

        :param vis: A VisConfiguration instance representing the visibility configuration.
        :return: An instance of LowCBFConfigurationBuilder with the set visibility configuration.
        """
        self.vis = vis
        return self

    def build(self) -> LowCBFConfiguration:
        """
        Builds or creates an instance of LowCBFConfiguration with the set properties.
        :return: An instance of LowCBFConfiguration with the specified configurations.
        """
        return LowCBFConfiguration(stations=self.stations, vis=self.vis)


class StationConfigurationBuilder:
    """
    StationConfigurationBuilder is a test data builder for StationConfiguration objects.
    """

    def __init__(self):
        self.stns = None
        self.stn_beams = None

    def set_stns(self, stns: List[List[int]]) -> "StationConfigurationBuilder":
        """
        Set the stations configuration.

        :param stns: A list of lists, where each inner list represents a station configuration.
        :return: An instance of StationConfigurationBuilder with the set stations configuration.
        """
        self.stns = stns
        return self

    def set_stn_beams(
        self, stn_beams: List[StnBeamConfiguration]
    ) -> "StationConfigurationBuilder":
        """
        Set the station beams configuration.

        :param stn_beams: A list of StnBeamConfiguration instances representing the station beams configuration.
        :return: An instance of StationConfigurationBuilder with the set station beams configuration.
        """
        self.stn_beams = stn_beams
        return self

    def build(self) -> StationConfiguration:
        """
        Builds or creates an instance of StationConfiguration with the set properties.
        :return: An instance of StationConfiguration with the specified configurations.
        """
        return StationConfiguration(stns=self.stns, stn_beams=self.stn_beams)


class StnBeamConfigurationBuilder:
    """
    StnBeamConfigurationBuilder is a test data builder for StnBeamConfiguration objects.
    """

    def __init__(self):
        self.stn_beam_id = None
        self.freq_ids = None
        self.host = None
        self.port = None
        self.mac = None
        self.integration_ms = None

    def set_stn_beam_id(self, stn_beam_id: int) -> "StnBeamConfigurationBuilder":
        """
        Set the station beam ID.

        :param stn_beam_id: Integer representing the station beam ID.
        :return: An instance of StnBeamConfigurationBuilder with the set station beam ID.
        """
        self.stn_beam_id = stn_beam_id
        return self

    def set_freq_ids(self, freq_ids: List[int]) -> "StnBeamConfigurationBuilder":
        """
        Set the frequency IDs for the station beam.

        :param freq_ids: A list of integers representing the frequency IDs.
        :return: An instance of StnBeamConfigurationBuilder with the set frequency IDs.
        """
        self.freq_ids = freq_ids
        return self

    def set_host(self, host: List[Tuple[int, str]]) -> "StnBeamConfigurationBuilder":
        """
        Set the host information for the station beam.

        :param host: A list of tuples, where each tuple contains an integer and a string representing the host information.
        :return: An instance of StnBeamConfigurationBuilder with the set host information.
        """
        self.host = host
        return self

    def set_port(
        self, port: List[Tuple[int, int, int]]
    ) -> "StnBeamConfigurationBuilder":
        """
        Set the port information for the station beam.

        :param port: A list of tuples, where each tuple contains three integers representing the port information.
        :return: An instance of StnBeamConfigurationBuilder with the set port information.
        """
        self.port = port
        return self

    def set_mac(self, mac: List[Tuple[int, str]]) -> "StnBeamConfigurationBuilder":
        """
        Set the MAC address information for the station beam.

        :param mac: A list of tuples, where each tuple contains an integer and a string representing the MAC address information.
        :return: An instance of StnBeamConfigurationBuilder with the set MAC address information.
        """
        self.mac = mac
        return self

    def set_integration_ms(self, integration_ms: int) -> "StnBeamConfigurationBuilder":
        """
        Set the integration time in milliseconds for the station beam.

        :param integration_ms: Integer representing the integration time in milliseconds.
        :return: An instance of StnBeamConfigurationBuilder with the set integration time.
        """
        self.integration_ms = integration_ms
        return self

    def build(self) -> StnBeamConfiguration:
        """
        Builds or creates an instance of StnBeamConfiguration with the set properties.
        :return: An instance of StnBeamConfiguration with the specified configurations.
        """
        return StnBeamConfiguration(
            stn_beam_id=self.stn_beam_id,
            freq_ids=self.freq_ids,
            host=self.host,
            port=self.port,
            mac=self.mac,
            integration_ms=self.integration_ms,
        )


class VisFspConfigurationBuilder:
    """
    VisFspConfigurationBuilder is a test data builder for VisFspConfiguration objects.
    """

    def __init__(self):
        self.function_mode = None
        self.fsp_ids = None

    def set_function_mode(self, function_mode: str) -> "VisFspConfigurationBuilder":
        """
        Set the function mode for the visibility FSP.

        :param function_mode: A string representing the function mode of the visibility FSP.
        """
        self.function_mode = function_mode
        return self

    def set_fsp_ids(self, fsp_ids: List[int]) -> "VisFspConfigurationBuilder":
        """
        Set the FSP IDs for the visibility FSP configuration.

        :param fsp_ids: A list of integers representing the FSP IDs.
        """
        self.fsp_ids = fsp_ids
        return self

    def build(self) -> VisFspConfiguration:
        """
        Builds or creates an instance of VisFspConfiguration with the set properties.
        :return: An instance of VisFspConfiguration with the specified configurations.
        """
        return VisFspConfiguration(
            function_mode=self.function_mode, fsp_ids=self.fsp_ids
        )


class VisConfigurationBuilder:
    """
    VisConfigurationBuilder is a test data builder for VisConfiguration objects.
    """

    def __init__(self):
        self.fsp = None
        self.stn_beams = None

    def set_fsp(self, fsp: VisFspConfiguration) -> "VisConfigurationBuilder":
        """
        Set the visibility FSP configuration.

        :param fsp: A VisFspConfiguration instance representing the visibility FSP configuration.
        :return: An instance of VisConfigurationBuilder with the set visibility FSP configuration.
        """
        self.fsp = fsp
        return self

    def set_stn_beam(
        self, stn_beams: List[StnBeamConfiguration]
    ) -> "VisConfigurationBuilder":
        """
        Set the station beam configuration to the visibility configuration.

        :param stn_beams: list of StnBeamConfiguration instance to be added to the visibility configuration.
        :return: An instance of VisConfigurationBuilder with the added station beam configuration.
        """

        self.stn_beams = stn_beams
        return self

    def build(self) -> VisConfiguration:
        """
        Builds or creates an instance of VisConfiguration with the set properties.
        :return: An instance of VisConfiguration with the specified configurations.
        """
        return VisConfiguration(fsp=self.fsp, stn_beams=self.stn_beams)


class CSPConfigurationBuilder:
    """
    CSPConfigurationBuilder is a test data builder for CSPConfiguration objects.

    This builder helps in creating instances of CSPConfiguration with custom settings for
    testing or any other purpose. It follows a fluent interface pattern allowing
    chaining of set methods.
    """

    def __init__(self):
        self.interface = None
        self.subarray = None
        self.common = None
        self.cbf_config = None
        self.pst_config = None
        self.pss_config = None
        self.lowcbf = None

    def set_interface(self, interface: str) -> "CSPConfigurationBuilder":
        """
        Set the interface version for the CSP configuration.
        :param interface: Interface version URL string.
        """
        self.interface = interface
        return self

    def set_subarray(
        self, subarray: SubarrayConfiguration
    ) -> "CSPConfigurationBuilder":
        """
        Set the SubarrayConfiguration.
        :param subarray: An instance of SubarrayConfiguration.
        """
        self.subarray = subarray
        return self

    def set_common(self, common: CommonConfiguration) -> "CSPConfigurationBuilder":
        """
        Set the CommonConfiguration.
        :param common: An instance of CommonConfiguration.
        """
        self.common = common
        return self

    def set_cbf_config(self, cbf_config: CBFConfiguration) -> "CSPConfigurationBuilder":
        """
        Set the CBFConfiguration.
        :param cbf_config: An instance of CBFConfiguration.
        """
        self.cbf_config = cbf_config
        return self

    def set_pst_config(
        self, pst_config: PSTConfiguration | dict
    ) -> "CSPConfigurationBuilder":
        """
        Set the PSTConfiguration.
        :param pst_config: An instance of PSTConfiguration or dict for backward compatibility.
        """
        self.pst_config = pst_config
        return self

    def set_pss_config(
        self, pss_config: PSSConfiguration | dict
    ) -> "CSPConfigurationBuilder":
        """
        Set the PSSConfiguration.
        :param pss_config: An instance of PSSConfiguration or dict for backward compatibility.
        """
        self.pss_config = pss_config
        return self

    def set_lowcbf(self, lowcbf: LowCBFConfiguration) -> "CSPConfigurationBuilder":
        """
        Set the LowCBFConfiguration.
        :param lowcbf: An instance of LowCBFConfiguration.
        """
        self.lowcbf = lowcbf
        return self

    def build(self) -> CSPConfiguration:
        """
        Builds and returns an instance of CSPConfiguration.
        """
        return CSPConfiguration(
            interface=self.interface,
            subarray=self.subarray,
            common=self.common,
            cbf_config=self.cbf_config,
            pst_config=self.pst_config,
            pss_config=self.pss_config,
            lowcbf=self.lowcbf,
        )

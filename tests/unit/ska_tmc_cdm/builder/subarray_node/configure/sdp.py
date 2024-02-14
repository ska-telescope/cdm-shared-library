from ska_tmc_cdm.messages.subarray_node.configure.sdp import SCHEMA, SDPConfiguration


class SDPConfigurationBuilder:
    def __init__(self):
        self.interface = SCHEMA
        self.scan_type = None

    def set_interface(self, interface: str) -> "SDPConfigurationBuilder":
        """
        Set the interface version for the SDP configuration.
        :param interface: Interface version URL string.
        """
        self.interface = interface
        return self

    def set_scan_type(self, scan_type: str) -> "SDPConfigurationBuilder":
        """
        Set the scan type for the SDP configuration.
        :param scan_type: Scan type string.
        """
        self.scan_type = scan_type
        return self

    def build(self):
        """
        Build or create SDP configuration
        :return: CDM SDP configuration instance
        """
        return SDPConfiguration(interface=self.interface, scan_type=self.scan_type)

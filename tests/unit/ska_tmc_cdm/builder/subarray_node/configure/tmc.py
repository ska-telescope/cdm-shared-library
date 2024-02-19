from datetime import timedelta

from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration


class TMCConfigurationBuilder:
    """
    TMCConfigurationBuilder is a test data builder for TMCConfiguration objects.
    """

    def __init__(self):
        self.scan_duration = None
        self.partial_configuration = False

    def set_scan_duration(self, scan_duration: timedelta) -> "TMCConfigurationBuilder":
        """
        Set the scan duration for the TMC configuration.
        :param scan_duration: A timedelta object representing the duration of the scan.
        """
        self.scan_duration = scan_duration
        return self

    def set_partial_configuration(
        self, partial_configuration: bool
    ) -> "TMCConfigurationBuilder":
        """
        Set the partial configuration flag for the TMC configuration.
        :param partial_configuration: A boolean indicating if the configuration should be marked as partial.
        """
        self.partial_configuration = partial_configuration
        return self

    def build(self) -> TMCConfiguration:
        """
        Builds or creates an instance of TMCConfiguration with the set properties.
        :return: An instance of TMCConfiguration with the specified configurations.
        """
        return TMCConfiguration(
            scan_duration=self.scan_duration,
            partial_configuration=self.partial_configuration,
        )

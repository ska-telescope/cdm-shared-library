from ska_tmc_cdm.messages.central_node.csp import (
    CSPConfiguration,
    PSSConfiguration,
    PSTConfiguration,
)


class PSSConfigurationBuilder:
    """
    PSSConfigurationBuilder is a test data builder for CDM PSSConfiguration
    objects.
    """

    def __init__(self) -> "PSSConfigurationBuilder":
        self.pss_beam_ids = None

    def set_pss_beam_ids(
        self, pss_beam_ids: list
    ) -> "PSSConfigurationBuilder":
        """
        Set the PSS
        :param pss: pss beam id for set.
        """
        self.pss_beam_ids = pss_beam_ids
        return self

    def build(self) -> PSSConfiguration:
        """
        Build or create CDM PSSConfiguration object
        :return: CDM PSSConfiguration object
        """
        return PSSConfiguration(pss_beam_ids=self.pss_beam_ids)


class PSTConfigurationBuilder:
    """
    PSTConfigurationBuilder is a test data builder for CDM PSTConfiguration
    objects.
    """

    def __init__(self) -> "PSTConfigurationBuilder":
        self.pst_beam_ids = None

    def set_pst_beam_ids(
        self, pst_beam_ids: list
    ) -> "PSTConfigurationBuilder":
        """
        Set the PST
        :param pst: pst beam id for set.
        """
        self.pst_beam_ids = pst_beam_ids
        return self

    def build(self) -> PSTConfiguration:
        """
        Build or create CDM PSTConfiguration object
        :return: CDM PSTConfiguration object
        """
        return PSTConfiguration(pst_beam_ids=self.pst_beam_ids)


# create class give name as CSPConfigurationBuilder and add pss and pst as attribute


class CSPConfigurationBuilder:
    """
    CSPConfigurationBuilder is a test data builder for CDM CSPConfiguration
    objects.
    """

    def __init__(self) -> "CSPConfigurationBuilder":
        self.pss = None
        self.pst = None

    def set_pss(self, pss: PSSConfiguration) -> "CSPConfigurationBuilder":
        """
        Set the PSS
        :param pss: pss configuration for set.
        """
        self.pss = pss
        return self

    def set_pst(self, pst: PSTConfiguration) -> "CSPConfigurationBuilder":
        """
        Set the PST
        :param pst: pst configuration for set.
        """
        self.pst = pst
        return self

    def build(self) -> CSPConfiguration:
        """
        Build or create CDM CSPConfiguration object
        :return: CDM CSPConfiguration object
        """
        return CSPConfiguration(pss=self.pss, pst=self.pst)

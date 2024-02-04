from ska_tmc_cdm.messages.central_node.sdp import SDPConfiguration
from ska_tmc_cdm.messages.subarray_node.configure import (
    ConfigureRequest,
    DishConfiguration,
    PointingConfiguration,
)
from ska_tmc_cdm.messages.subarray_node.configure.csp import CSPConfiguration
from ska_tmc_cdm.messages.subarray_node.configure.mccs import MCCSConfiguration
from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration


class ConfigureRequestBuilder:
    """
    ConfigureRequestBuilder is a test data builder for ConfigureRequest objects.
    """

    def __init__(self):
        self.pointing = None
        self.dish = None
        self.sdp = None
        self.csp = None
        self.mccs = None
        self.tmc = None
        self.interface = None
        self.transaction_id = None

    def set_pointing(
        self, pointing: PointingConfiguration
    ) -> "ConfigureRequestBuilder":
        """
        Set pointing configuration
        :param: pointing: PointingConfiguration
        """
        self.pointing = pointing
        return self

    def set_dish(self, dish: DishConfiguration) -> "ConfigureRequestBuilder":
        """
        Set dish configuration
        :param: dish: DishConfiguration
        """
        self.dish = dish
        return self

    def set_sdp(self, sdp: SDPConfiguration) -> "ConfigureRequestBuilder":
        """
        Set sdp configuration
        :param: sdp: SDPConfiguration
        """
        self.sdp = sdp
        return self

    def set_csp(self, csp: CSPConfiguration) -> "ConfigureRequestBuilder":
        """
        Set csp configuration
        :param: csp: CSPConfiguration
        """
        self.csp = csp
        return self

    def set_mccs(self, mccs: MCCSConfiguration) -> "ConfigureRequestBuilder":
        """
        Set mccs configuration
        :param: mccs: MCCSConfiguration
        """
        self.mccs = mccs
        return self

    def set_tmc(self, tmc: TMCConfiguration) -> "ConfigureRequestBuilder":
        """
        Set tmc configuration
        :param: tmc: TMCConfiguration
        :raises ValueError: if tmc is allocated with dish and sdp
        """
        self.tmc = tmc
        return self

    def set_interface(self, interface: str) -> "ConfigureRequestBuilder":
        """
        Set interface version
        :param: interface: Interface version
        """
        self.interface = interface
        return self

    def set_transaction_id(self, transaction_id: str) -> "ConfigureRequestBuilder":
        """
        Set transaction ID
        :param: transaction_id: Transaction ID
        """
        self.transaction_id = transaction_id
        return self

    def build(self) -> ConfigureRequest:
        """
        Builds or creates an instance of ConfigureRequest.
        :return: CDM ConfigureRequest
        """
        return ConfigureRequest(
            pointing=self.pointing,
            dish=self.dish,
            sdp=self.sdp,
            csp=self.csp,
            mccs=self.mccs,
            tmc=self.tmc,
            interface=self.interface,
            transaction_id=self.transaction_id,
        )

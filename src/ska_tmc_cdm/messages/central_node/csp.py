"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import Dict, List

__all__ = [
    "CSPLowConfiguration",
]


class CSPLowConfiguration:
    """
    Class to get CSP Configuration
    """

    def check(self, my_iface, my_sid, my_lowcbf):
        """
        internal function that
        raises key error by default
        and custom type errors for values
        """
        # check interface
        if isinstance(my_iface, str) is False:
            raise TypeError("key 'interface' takes str value")
        # check subarray_id in common
        if isinstance(my_sid["subarray_id"], int) is False:
            raise TypeError("key 'subarray_id' takes a int")
        # check fields in lowcbf
        my_dict = my_lowcbf["resources"]  # list of nested dict
        for lst in my_dict:
            temp_dict = dict(lst)
            if isinstance(temp_dict["device"], str) is False:
                raise TypeError("key 'device' takes str value")
            if isinstance(temp_dict["shared"], bool) is False:
                raise TypeError("key 'shared' takes bool value")
            if isinstance(temp_dict["fw_image"], str) is False:
                raise TypeError("key 'fw_image' takes str value")
            if isinstance(temp_dict["fw_mode"], str) is False:
                raise TypeError("key 'fw_mode' takes str value")

    def __init__(
        self,
        interface: str = None,
        common: Dict[str, int] = None,
        lowcbf: Dict[str, List[Dict]] = None,
    ) -> object:

        """
        Create a new CSPLowConfiguration object.

        :param interface:
        :param common:
        :param lowcbf:
        """
        self.check(my_iface=interface, my_sid=common, my_lowcbf=lowcbf)
        # if no error raised
        self.interface = interface
        self.common = common
        self.lowcbf = lowcbf

    def __eq__(self, other):
        if not isinstance(other, CSPLowConfiguration):
            return False
        return (
            self.interface == other.interface
            and self.common == other.common
            and self.lowcbf == other.lowcbf
        )

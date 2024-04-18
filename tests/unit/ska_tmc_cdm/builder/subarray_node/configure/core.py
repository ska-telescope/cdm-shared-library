from typing import Union

from astropy import units as u

from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    PointingConfiguration,
    ReceiverBand,
    Target,
    UnitStr,
)


class TargetBuilder:
    """
    TargetBuilder is a test data builder for Target objects.
    """

    def __init__(self):
        self.ra = None
        self.dec = None
        self.target_name = ""
        self.reference_frame = "icrs"
        self.unit = (
            u.hourangle,
            u.deg,
        )
        self.ca_offset_arcsec = 0.0
        self.ie_offset_arcsec = 0.0

    def set_ra(
        self, ra: Union[str, int, float, u.Quantity]
    ) -> "TargetBuilder":
        """
        Set right ascension.
        :param ra: Right ascension, can be a string, integer, float, or astropy Quantity.
        """
        self.ra = ra
        return self

    def set_dec(
        self, dec: Union[str, int, float, u.Quantity]
    ) -> "TargetBuilder":
        """
        Set declination.
        :param dec: Declination, can be a string, integer, float, or astropy Quantity.
        """
        self.dec = dec
        return self

    def set_target_name(self, target_name: str) -> "TargetBuilder":
        """
        Set target name.
        :param target_name: Target name.
        """
        self.target_name = target_name
        return self

    def set_reference_frame(self, reference_frame: str) -> "TargetBuilder":
        """
        Set reference frame.
        :param reference_frame: Target coordinate reference frame.
        """
        self.reference_frame = reference_frame
        return self

    def set_unit(
        self, unit: Union[UnitStr, tuple[UnitStr, UnitStr]]
    ) -> "TargetBuilder":
        """
        Set the unit of RA and Dec.
        :param unit: The unit for RA/Dec, can be a single unit or a tuple of units.
        """
        self.unit = unit
        return self

    def set_ca_offset_arcsec(self, ca_offset_arcsec: float) -> "TargetBuilder":
        """
        Set CA offset in arcseconds.
        :param ca_offset_arcsec: CA offset in arcseconds.
        """
        self.ca_offset_arcsec = ca_offset_arcsec
        return self

    def set_ie_offset_arcsec(self, ie_offset_arcsec: float) -> "TargetBuilder":
        """
        Set IE offset in arcseconds.
        :param ie_offset_arcsec: IE offset in arcseconds.
        """
        self.ie_offset_arcsec = ie_offset_arcsec
        return self

    def build(self) -> Target:
        """
        Build or create a Target instance.
        :return: A Target instance with the specified configurations.
        """

        return Target(
            ra=self.ra,
            dec=self.dec,
            target_name=self.target_name,
            reference_frame=self.reference_frame,
            unit=self.unit,
            ca_offset_arcsec=self.ca_offset_arcsec,
            ie_offset_arcsec=self.ie_offset_arcsec,
        )


class PointingConfigurationBuilder:
    """
    PointingConfigurationBuilder is a test data builder for PointingConfiguration objects.
    """

    def __init__(self):
        self.target = None

    def set_target(self, target: Target) -> "PointingConfigurationBuilder":
        """
        Set target
        :param: target: Target instance
        """
        self.target = target
        return self

    def build(self) -> "PointingConfiguration":
        """
        Build or create pointing configuration
        :return: CDM pointing configuration instance
        """
        return PointingConfiguration(target=self.target)


class DishConfigurationBuilder:
    """
    DishConfigurationBuilder is a test data builder for DishConfiguration objects.
    """

    def __init__(self):
        self.receiver_band = None

    def set_receiver_band(
        self, receiver_band: ReceiverBand
    ) -> "DishConfigurationBuilder":
        """
        Set receiver band
        :param: receiver_band: receiver band
        """
        self.receiver_band = receiver_band
        return self

    def build(self) -> "DishConfiguration":
        """
        Build or create dish configuration
        :return: CDM dish configuration instance
        """
        return DishConfiguration(receiver_band=self.receiver_band)

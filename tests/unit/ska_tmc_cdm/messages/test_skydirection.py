from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import ValidationError

from ska_tmc_cdm.messages.skydirection import (
    AltAzField,
    GalacticField,
    ICRSField,
)


class TestICRSField:
    @pytest.mark.parametrize(
        "c1,c2,expectation",
        [
            pytest.param(0.0, -90.0, does_not_raise(), id="all at min limits"),
            pytest.param(
                359.999, 90.0, does_not_raise(), id="all at max limits"
            ),
            pytest.param(
                -0.1, 0.0, pytest.raises(ValidationError), id="c1 < 0.0"
            ),
            pytest.param(
                360.0, 0.0, pytest.raises(ValidationError), id="c1 >= 360.0"
            ),
            pytest.param(
                0.0, -90.1, pytest.raises(ValidationError), id="c2 < -90.0"
            ),
            pytest.param(
                0.0, 90.1, pytest.raises(ValidationError), id="c2 > 90.0"
            ),
        ],
    )
    def test_limits(self, c1, c2, expectation):
        """
        Check that errors are raised when c1,c2 values exceed bounds.
        """
        with expectation:
            ICRSField(target_name="foo", attrs=ICRSField.Attrs(c1=c1, c2=c2))


class TestAltAzField:
    @pytest.mark.parametrize(
        "c1,c2,expectation",
        [
            pytest.param(0.0, 0.0, does_not_raise(), id="all at min limits"),
            pytest.param(
                359.999, 90.0, does_not_raise(), id="all at max limits"
            ),
            pytest.param(
                -0.1, 0.0, pytest.raises(ValidationError), id="c1 < 0.0"
            ),
            pytest.param(
                360.0, 0.0, pytest.raises(ValidationError), id="c1 >= 360.0"
            ),
            pytest.param(
                0.0, -0.1, pytest.raises(ValidationError), id="c2 < 0.0"
            ),
            pytest.param(
                0.0, 90.1, pytest.raises(ValidationError), id="c2 > 90.0"
            ),
        ],
    )
    def test_limits(self, c1, c2, expectation):
        """
        Check that errors are raised when c1,c2 values exceed bounds.
        """
        with expectation:
            AltAzField(target_name="foo", attrs=AltAzField.Attrs(c1=c1, c2=c2))


class TestGalacticField:
    @pytest.mark.parametrize(
        "c1,c2,expectation",
        [
            pytest.param(0.0, -90.0, does_not_raise(), id="all at min limits"),
            pytest.param(
                359.999, 90.0, does_not_raise(), id="all at max limits"
            ),
            pytest.param(
                -0.1, 0.0, pytest.raises(ValidationError), id="c1 < 0.0"
            ),
            pytest.param(
                360.0, 0.0, pytest.raises(ValidationError), id="c1 >= 360.0"
            ),
            pytest.param(
                0.0, -90.1, pytest.raises(ValidationError), id="c2 < -90.0"
            ),
            pytest.param(
                0.0, 90.1, pytest.raises(ValidationError), id="c2 > 90.0"
            ),
        ],
    )
    def test_limits(self, c1, c2, expectation):
        """
        Check that errors are raised when c1,c2 values exceed bounds.
        """
        with expectation:
            GalacticField(
                target_name="foo", attrs=GalacticField.Attrs(c1=c1, c2=c2)
            )

from contextlib import nullcontext as does_not_raise
from itertools import product

import pytest
from pydantic import BaseModel, ValidationError

from ska_tmc_cdm import CODEC
from ska_tmc_cdm.messages.skydirection import (
    AltAzField,
    GalacticField,
    ICRSField,
    SkyDirection,
    SolarSystemObject,
    SpecialField,
    TLEField,
)
from ska_tmc_cdm.utils import assert_json_is_equal


class TestICRSField:
    FULL_JSON = """
    {
        "target_name": "foo",
        "reference_frame": "icrs",
        "attrs": {
            "c1": 1.23,
            "c2": -4.56,
            "pm_c1": 1.0,
            "pm_c2": 2.0,
            "epoch": 2000.0,
            "parallax": 3.0,
            "radial_velocity": 4.0
        }
    }
    """

    MINIMAL_JSON = """
    {
        "target_name": "foo",
        "reference_frame": "icrs",
        "attrs": {
            "c1": 1.23,
            "c2": -4.56
        }
    }
    """

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

    def test_full_instance_round_trip(self):
        """
        Test serialisation and deserialisation of a fully-defined ICRSField.
        """
        instance = ICRSField(
            target_name="foo",
            attrs=ICRSField.Attrs(
                c1=1.23,
                c2=-4.56,
                pm_c1=1.0,
                pm_c2=2.0,
                epoch=2000.0,
                parallax=3.0,
                radial_velocity=4.0,
            ),
        )
        assert_json_is_equal(TestICRSField.FULL_JSON, CODEC.dumps(instance))
        assert instance == CODEC.loads(ICRSField, TestICRSField.FULL_JSON)

    def test_partial_instance_round_trip(self):
        """
        Round trip to confirm successful serialisation and deserialisation of
        the smallest possible ICRS field where only mandatory attributes are
        defined.

        This checks that optionals with defaults have not sneaked into the
        schema.
        """
        instance = ICRSField(
            target_name="foo", attrs=ICRSField.Attrs(c1=1.23, c2=-4.56)
        )
        assert_json_is_equal(TestICRSField.MINIMAL_JSON, CODEC.dumps(instance))
        assert instance == CODEC.loads(ICRSField, TestICRSField.MINIMAL_JSON)


class TestAltAzField:
    JSON = """
        {
            "target_name": "foo",
            "reference_frame": "altaz",
            "attrs": {
                "c1": 1.23,
                "c2": 4.56
            }
        }
    """

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

    def test_full_instance_round_trip(self):
        """
        Test serialisation and deserialisation of an AltAzField.
        """
        instance = AltAzField(
            target_name="foo", attrs=AltAzField.Attrs(c1=1.23, c2=4.56)
        )
        assert_json_is_equal(TestAltAzField.JSON, CODEC.dumps(instance))
        assert instance == CODEC.loads(AltAzField, TestAltAzField.JSON)


class TestGalacticField:
    FULL_JSON = """
        {
            "target_name": "foo",
            "reference_frame": "galactic",
            "attrs": {
                "c1": 1.23,
                "c2": -4.56,
                "pm_c1": 1.0,
                "pm_c2": 2.0,
                "epoch": 2000.0,
                "parallax": 3.0,
                "radial_velocity": 4.0
            }
        }
    """

    MINIMAL_JSON = """
    {
        "target_name": "foo",
        "reference_frame": "galactic",
        "attrs": {
            "c1": 1.23,
            "c2": -4.56
        }
    }
    """

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

    def test_full_instance_round_trip(self):
        """
        Test serialisation and deserialisation of a fully-defined
        GalacticField.
        """
        instance = GalacticField(
            target_name="foo",
            attrs=GalacticField.Attrs(
                c1=1.23,
                c2=-4.56,
                pm_c1=1.0,
                pm_c2=2.0,
                epoch=2000.0,
                parallax=3.0,
                radial_velocity=4.0,
            ),
        )
        assert_json_is_equal(
            TestGalacticField.FULL_JSON, CODEC.dumps(instance)
        )
        assert instance == CODEC.loads(
            GalacticField, TestGalacticField.FULL_JSON
        )

    def test_partial_instance_round_trip(self):
        """
        Test round-trip serialisation of a minimally-defined GalacticField.
        This checks that optional fields do not have default values.
        """
        instance = GalacticField(
            target_name="foo", attrs=GalacticField.Attrs(c1=1.23, c2=-4.56)
        )
        assert_json_is_equal(
            TestGalacticField.MINIMAL_JSON, CODEC.dumps(instance)
        )
        assert instance == CODEC.loads(
            GalacticField, TestGalacticField.MINIMAL_JSON
        )


class TestSpecialField:
    FULL_JSON = """
    {
        "target_name": "Venus",
        "reference_frame": "special"
    }
    """

    @pytest.mark.parametrize(
        "target_name,expectation",
        [
            pytest.param("mars", does_not_raise(), id="all lower-case"),
            pytest.param("MARS", does_not_raise(), id="all upper-case"),
            pytest.param("mArS", does_not_raise(), id="mixed-case"),
            pytest.param(
                "foo", pytest.raises(ValidationError), id="Invalid source"
            ),
        ],
    )
    def test_deserialisation_is_case_insensitive(
        self, target_name: str, expectation
    ):
        """
        Confirms that the class is lenient when deserialising target names,
        ignoring case when creating the target_name enum value.
        """
        expected = SpecialField(target_name=SolarSystemObject.MARS)
        deserialised = f"""
        {{
            "target_name": "{target_name}",
            "reference_frame": "special"
        }}
        """
        with expectation:
            actual = CODEC.loads(SpecialField, deserialised)
            assert actual == expected

    def test_round_trip(self):
        """
        Test serialisation and deserialisation of a fully-defined
        SpecialField.

        Note that the target_name should be serialised to exact Enum value,
        i.e., a capitalised proper noun.
        """
        instance = SpecialField(target_name=SolarSystemObject.VENUS)
        assert_json_is_equal(TestSpecialField.FULL_JSON, CODEC.dumps(instance))
        assert instance == CODEC.loads(
            SpecialField, TestSpecialField.FULL_JSON
        )


class TestTLEField:
    FULL_JSON = """
        {
            "target_name": "foo",
            "reference_frame": "tle",
            "attrs": {
                "line1": [1.0, 2.0],
                "line2": [3.0, 4.0]
            }
        }
    """

    def test_full_instance_round_trip(self):
        """
        Test serialisation and deserialisation of a fully-defined TLEField.
        """
        instance = TLEField(
            target_name="foo",
            attrs=TLEField.Attrs(line1=[1.0, 2.0], line2=[3.0, 4.0]),
        )
        assert_json_is_equal(TestTLEField.FULL_JSON, CODEC.dumps(instance))
        assert instance == CODEC.loads(TLEField, TestTLEField.FULL_JSON)


def case_permutations(val: str) -> list[str]:
    """
    Return all possible permutations in case of an input value.

    Example:

        'ab' -> ['ab', 'aB', 'Ab', 'AB']
    """
    cases = zip(*[val, val.swapcase()])
    return ["".join(permutation) for permutation in product(*cases)]


class TestSkyDirection:
    @pytest.mark.parametrize("new_frame", [*case_permutations("tle")])
    def test_case_insensitive_discriminator(self, new_frame):
        class TestModel(BaseModel):
            field: SkyDirection

        input_json = f"""
            {{
                "field": {TestTLEField.FULL_JSON.replace('tle', new_frame)}
            }}
        """

        # ValidationError would be raised if Enum not recognised
        TestModel.model_validate_json(input_json)

    @pytest.mark.parametrize(
        "json_str,cls",
        [
            (TestICRSField.FULL_JSON, ICRSField),
            (TestICRSField.MINIMAL_JSON, ICRSField),
            (TestAltAzField.JSON, AltAzField),
            (TestGalacticField.FULL_JSON, GalacticField),
            (TestGalacticField.MINIMAL_JSON, GalacticField),
            (TestSpecialField.FULL_JSON, SpecialField),
            (TestTLEField.FULL_JSON, TLEField),
        ],
    )
    def test_correct_class_is_created_without_discriminator(
        self, json_str, cls
    ):
        """
        Verify that the expected class is created when deserialising a
        SkyDirection Union, even though that Union does not contain a
        discriminator.
        """

        class TestModel(BaseModel):
            field: SkyDirection

        input_json = f"""
            {{
                "field": {json_str}
            }}
        """

        instance = TestModel.model_validate_json(input_json)
        assert isinstance(instance.field, cls)

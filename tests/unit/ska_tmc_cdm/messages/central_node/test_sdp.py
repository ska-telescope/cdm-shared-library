"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
import copy
from typing import NamedTuple

import pytest

from ska_tmc_cdm.messages.central_node.sdp import PhaseDir
from tests.unit.ska_tmc_cdm.builder.central_node.sdp import (
    BeamConfigurationBuilder,
    ChannelBuilder,
    EBScanTypeBeamBuilder,
    EBScanTypeBuilder,
    ExecutionBlockConfigurationBuilder,
    FieldConfigurationBuilder,
    PbDependencyBuilder,
    PhaseDirBuilder,
    PolarisationConfigurationBuilder,
    ProcessingBlockConfigurationBuilder,
    ScanTypeBuilder,
    ScriptConfigurationBuilder,
    SDPConfigurationBuilder,
    SDPWorkflowBuilder,
)


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            ChannelBuilder(),
            ChannelBuilder(),
            True,
        ),
        (  # not equal
            ChannelBuilder(stride=1),
            ChannelBuilder(stride=2),  # different stride value
            False,
        ),
    ],
)
def test_channel_equality(object1, object2, is_equal):
    """
    Verify that Channel objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            ScanTypeBuilder(),
            ScanTypeBuilder(),
            True,
        ),
        (  # not equal
            ScanTypeBuilder(scan_type_id="science_A"),
            ScanTypeBuilder(scan_type_id="science_B"),
            False,
        ),
    ],
)
def test_scan_type_equality(object1, object2, is_equal):
    """
    Verify that ScanType  objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            SDPWorkflowBuilder(),
            SDPWorkflowBuilder(),
            True,
        ),
        (  # not equal
            SDPWorkflowBuilder(version="0.1.1"),
            SDPWorkflowBuilder(version="0.0.1"),
            False,
        ),
    ],
)
def test_workflow_equality(object1, object2, is_equal):
    """
    Verify that SDPWorkflow objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            PbDependencyBuilder(),
            PbDependencyBuilder(),
            True,
        ),
        (  # not_equal
            PbDependencyBuilder(pb_id="pb-mvp01-20200325-00001"),
            PbDependencyBuilder(
                pb_id="pb-mvp01-20200325-00002"
            ),  # different pb_id
            False,
        ),
    ],
)
def test_pb_dependency_equality(object1, object2, is_equal):
    """
    Verify that SDPWorkflow objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            ProcessingBlockConfigurationBuilder(
                dependencies=[PbDependencyBuilder()]
            ),
            ProcessingBlockConfigurationBuilder(
                dependencies=[PbDependencyBuilder()]
            ),
            True,
        ),
        (  # not equal
            ProcessingBlockConfigurationBuilder(
                dependencies=[
                    PbDependencyBuilder(pb_id="pb-mvp01-20200325-00001")
                ]
            ),
            ProcessingBlockConfigurationBuilder(
                dependencies=[
                    PbDependencyBuilder(pb_id="pb-mvp01-20200325-00003")
                ]
            ),  # different dependency
            False,
        ),
    ],
)
def test_processing_block_equality_check(object1, object2, is_equal):
    """
    Verify that SDPWorkflow objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


def test_sdp_equality_check():
    """
    Verify that SDP Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """
    sdp1 = SDPConfigurationBuilder()
    sdp2 = SDPConfigurationBuilder(
        interface="https://schema.skao.int/ska-sdp-assignres/0.3"
    )

    assert sdp1 == copy.deepcopy(sdp1)
    assert sdp1 != sdp2
    assert sdp1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            BeamConfigurationBuilder(),
            BeamConfigurationBuilder(),
            True,
        ),
        (  # not_equal
            BeamConfigurationBuilder(beam_id="pss1"),
            BeamConfigurationBuilder(beam_id="vis0"),
            False,
        ),
    ],
)
def test_beam_equality(object1, object2, is_equal):
    """
    Verify that Beam objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            ChannelBuilder(),
            ChannelBuilder(),
            True,
        ),
        (  # not_equal
            ChannelBuilder(start=0),
            ChannelBuilder(start=1),
            False,
        ),
    ],
)
def test_channel_configuration_equality(object1, object2, is_equal):
    """
    Verify that Channel Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            PolarisationConfigurationBuilder(),
            PolarisationConfigurationBuilder(),
            True,
        ),
        (  # not_equal
            PolarisationConfigurationBuilder(
                corr_type=["YY", "XY", "YY", "YX"]
            ),
            PolarisationConfigurationBuilder(
                corr_type=["XX", "XY", "YY", "YX"]
            ),
            False,
        ),
    ],
)
def test_polarisation_configuration_equality(object1, object2, is_equal):
    """
    Verify that Polarisation Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


class PhaseDirCase(NamedTuple):
    equal: bool
    pd1: PhaseDir
    pd2: PhaseDir


PHASEDIR_CASES = (
    PhaseDirCase(
        equal=True,
        pd1=PhaseDirBuilder(),
        pd2=PhaseDirBuilder(),
    ),
    PhaseDirCase(
        equal=True,
        pd1=PhaseDirBuilder(dec=[12.582438888888891]),
        # Very slightly different dec
        pd2=PhaseDirBuilder(dec=[12.582438888888893]),
    ),
    PhaseDirCase(
        equal=False,
        pd1=PhaseDirBuilder(reference_frame="ICRF3"),
        pd2=PhaseDirBuilder(reference_frame="ICRF4"),
    ),
    PhaseDirCase(
        equal=False,
        pd1=PhaseDirBuilder(ra=[123, 0.1]),
        pd2=PhaseDirBuilder(ra=[123, 2.1]),
    ),
)


@pytest.mark.parametrize(
    "expected_equal,phase_dir1,phase_dir2", PHASEDIR_CASES
)
def test_phase_dir_equals(
    expected_equal: bool, phase_dir1: PhaseDir, phase_dir2: PhaseDir
):
    """
    Verify that Phase Dir objects are considered equal when they have:
     - (almost) the same ra
     - (almost) the same dec (we use math.isclose() to allow for floating point math imprecision)
     - the same refrence_time
     - the same refrence_frame
    """
    if expected_equal:
        assert phase_dir1 == phase_dir2
    else:
        assert phase_dir1 != phase_dir2

    assert phase_dir1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            FieldConfigurationBuilder(),
            FieldConfigurationBuilder(),
            True,
        ),
        (  # not_equal
            FieldConfigurationBuilder(field_id="field_a"),
            FieldConfigurationBuilder(field_id="field_b"),
            False,
        ),
    ],
)
def test_field_configuration_equality(object1, object2, is_equal):
    """
    Verify that Field Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            EBScanTypeBuilder(),
            EBScanTypeBuilder(),
            True,
        ),
        (  # not_equal
            EBScanTypeBuilder(beams={"vis0": {"field_id": "field_a"}}),
            EBScanTypeBuilder(beams={"vis0": {"field_id": "field_b"}}),
            False,
        ),
    ],
)
def test_eb_scan_equality(object1, object2, is_equal):
    """
    Verify that EBScan Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            EBScanTypeBeamBuilder(),
            EBScanTypeBeamBuilder(),
            True,
        ),
        (  # not_equal
            EBScanTypeBeamBuilder(field_id="pss_field_1"),
            EBScanTypeBeamBuilder(field_id="pss_field_2"),
            False,
        ),
    ],
)
def test_eb_scan_type_beam_equality(object1, object2, is_equal):
    """
    Verify that EBScanTypeBeam Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            ScriptConfigurationBuilder(),
            ScriptConfigurationBuilder(),
            True,
        ),
        (  # not_equal
            ScriptConfigurationBuilder(version="0.5.0"),
            ScriptConfigurationBuilder(version="0.6.0"),  # different version
            False,
        ),
    ],
)
def test_script_equality(object1, object2, is_equal):
    """
    Verify that Script Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


def test_processing_block_equality():
    """
    Verify that Processing Block Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """

    pb1 = ProcessingBlockConfigurationBuilder(
        sbi_ids=["sbi-mvp01-20200325-00001"]
    )

    pb2 = ProcessingBlockConfigurationBuilder(
        sbi_ids=["sbi-mvp01-20200325-00003"]
    )  # different sbi_id

    assert pb1 == copy.deepcopy(pb1)
    assert pb1 != pb2
    assert pb1 != object()


def test_execution_block_configuration_equals():
    """
    Verify that Execution Block Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """

    execution_block1 = ExecutionBlockConfigurationBuilder(max_length=3600)
    execution_block2 = ExecutionBlockConfigurationBuilder(max_length=3400)

    assert execution_block1 == copy.deepcopy(execution_block1)
    assert execution_block1 != execution_block2
    assert execution_block1 != object()

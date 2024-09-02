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
            ScanTypeBuilder()
            .set_scan_type_id(scan_type_id="science_A")
            .set_reference_frame(reference_frame="ICRS")
            .set_ra(ra="02:42:40.771")
            .set_dec(dec="-00:00:47.84")
            .set_channels([ChannelBuilder()])
            .build(),
            ScanTypeBuilder()
            .set_scan_type_id(scan_type_id="science_A")
            .set_reference_frame(reference_frame="ICRS")
            .set_ra(ra="02:42:40.771")
            .set_dec(dec="-00:00:47.84")
            .set_channels([ChannelBuilder()])
            .build(),
            True,
        ),
        (  # not equal
            ScanTypeBuilder()
            .set_scan_type_id(scan_type_id="science_A")
            .set_reference_frame(reference_frame="ICRS")
            .set_ra(ra="02:42:40.771")
            .set_dec(dec="-00:00:47.84")
            .set_channels([ChannelBuilder()])
            .build(),
            ScanTypeBuilder()
            .set_scan_type_id(scan_type_id="science_B")  # different scan id
            .set_reference_frame(reference_frame="ICRS")
            .set_ra(ra="02:42:40.771")
            .set_dec(dec="-00:00:47.84")
            .set_channels([ChannelBuilder()])
            .build(),
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
            SDPWorkflowBuilder()
            .set_name(name="vis_receive")
            .set_kind(kind="realtime")
            .set_version(version="0.1.1")
            .build(),
            SDPWorkflowBuilder()
            .set_name(name="vis_receive")
            .set_kind(kind="realtime")
            .set_version(version="0.1.1")
            .build(),
            True,
        ),
        (  # not equal
            SDPWorkflowBuilder()
            .set_name(name="vis_receive")
            .set_kind(kind="realtime")
            .set_version(version="0.1.1")
            .build(),
            SDPWorkflowBuilder()
            .set_name(name="vis_receive")
            .set_kind(kind="realtime")
            .set_version(version="0.0.1")
            .build(),
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
            PbDependencyBuilder()
            .set_pb_id(pb_id="pb-mvp01-20200325-00001")
            .set_kind(kind=["visibilities"])
            .build(),
            PbDependencyBuilder()
            .set_pb_id(pb_id="pb-mvp01-20200325-00001")
            .set_kind(kind=["visibilities"])
            .build(),
            True,
        ),
        (  # not_equal
            PbDependencyBuilder()
            .set_pb_id(pb_id="pb-mvp01-20200325-00001")
            .set_kind(kind=["visibilities"])
            .build(),
            PbDependencyBuilder()
            .set_pb_id(pb_id="pb-mvp01-20200325-00002")
            .set_kind(kind=["visibilities"])
            .build(),  # different pb_id
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
            ProcessingBlockConfigurationBuilder()
            .set_pb_id(pb_id="pb-mvp01-20200325-00001")
            .set_workflow(
                SDPWorkflowBuilder()
                .set_name(name="vis_receive")
                .set_kind(kind="realtime")
                .set_version(version="0.1.1")
                .build()
            )
            .set_dependencies(
                [
                    PbDependencyBuilder()
                    .set_pb_id(pb_id="pb-mvp01-20200325-00001")
                    .set_kind(kind=["visibilities"])
                    .build()
                ]
            )
            .build(),
            ProcessingBlockConfigurationBuilder()
            .set_pb_id(pb_id="pb-mvp01-20200325-00001")
            .set_workflow(
                SDPWorkflowBuilder()
                .set_name(name="vis_receive")
                .set_kind(kind="realtime")
                .set_version(version="0.1.1")
                .build()
            )
            .set_dependencies(
                [
                    PbDependencyBuilder()
                    .set_pb_id(pb_id="pb-mvp01-20200325-00001")
                    .set_kind(kind=["visibilities"])
                    .build()
                ]
            )
            .build(),
            True,
        ),
        (  # not_equal
            ProcessingBlockConfigurationBuilder()
            .set_pb_id(pb_id="pb-mvp01-20200325-00001")
            .set_workflow(
                SDPWorkflowBuilder()
                .set_name(name="vis_receive")
                .set_kind(kind="realtime")
                .set_version(version="0.1.1")
                .build()
            )
            .set_dependencies(
                [
                    PbDependencyBuilder()
                    .set_pb_id(pb_id="pb-mvp01-20200325-00001")
                    .set_kind(kind=["visibilities"])
                    .build()
                ]
            )
            .build(),
            ProcessingBlockConfigurationBuilder()
            .set_pb_id(pb_id="pb-mvp01-20200325-00001")
            .set_workflow(
                SDPWorkflowBuilder()
                .set_name(name="vis_receive")
                .set_kind(kind="realtime")
                .set_version(version="0.1.1")
                .build()
            )
            .set_dependencies(
                [
                    PbDependencyBuilder()
                    .set_pb_id(pb_id="pb-mvp01-20200325-00003")
                    .set_kind(kind=["visibilities"])
                    .build()
                ]
            )  # different dependency
            .build(),
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


def test_sdp_equality_check(processing_block, execution_block):
    """
    Verify that SDP Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """
    sdp1 = (
        SDPConfigurationBuilder()
        .set_processing_blocks(processing_blocks=[processing_block])
        .set_execution_block(execution_block=execution_block)
        .build()
    )

    sdp2 = (
        SDPConfigurationBuilder()
        .set_interface("https://schema.skao.int/ska-sdp-assignres/0.3")
        .set_processing_blocks(processing_blocks=[processing_block])
        .set_execution_block(execution_block=execution_block)
        .build()
    )

    assert sdp1 == copy.deepcopy(sdp1)
    assert sdp1 != sdp2
    assert sdp1 != object()


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # equal
            BeamConfigurationBuilder()
            .set_beam_id(beam_id="pss1")
            .set_function(function="pulsar search")
            .set_search_beam_id(search_beam_id=1)
            .build(),
            BeamConfigurationBuilder()
            .set_beam_id(beam_id="pss1")
            .set_function(function="pulsar search")
            .set_search_beam_id(search_beam_id=1)
            .build(),
            True,
        ),
        (  # not_equal
            BeamConfigurationBuilder()
            .set_beam_id(beam_id="pss1")
            .set_function(function="pulsar search")
            .set_search_beam_id(search_beam_id=1)
            .build(),
            BeamConfigurationBuilder()
            .set_beam_id(beam_id="vis0")  # different beam id
            .set_function(function="pulsar search")
            .set_search_beam_id(search_beam_id=1)
            .build(),
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
            PolarisationConfigurationBuilder()
            .set_polarisations_id(polarisations_id="all")
            .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
            .build(),
            PolarisationConfigurationBuilder()
            .set_polarisations_id(polarisations_id="all")
            .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
            .build(),
            True,
        ),
        (  # not_equal
            PolarisationConfigurationBuilder()
            .set_polarisations_id(polarisations_id="all")
            .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
            .build(),
            PolarisationConfigurationBuilder()
            .set_polarisations_id(polarisations_id="all")
            .set_corr_type(
                corr_type=["YY", "XY", "YY", "YX"]
            )  # different corr_type value
            .build(),
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
        pd1=PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build(),
        pd2=PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build(),
    ),
    PhaseDirCase(
        equal=True,
        pd1=PhaseDirBuilder()
        .set_ra(ra=[188.73658333333333])
        .set_dec(dec=[12.582438888888891])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build(),
        pd2=PhaseDirBuilder()
        .set_ra(ra=[188.73658333333333])
        .set_dec(dec=[12.582438888888893])  # Very slightly different dec
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build(),
    ),
    PhaseDirCase(
        equal=False,
        pd1=PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build(),
        pd2=PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF4")  # Different frame
        .build(),
    ),
    PhaseDirCase(
        equal=False,
        pd1=PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build(),
        pd2=PhaseDirBuilder()
        .set_ra(ra=[123, 2.1])  # Different RA
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build(),
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
            FieldConfigurationBuilder()
            .set_field_id(field_id="field_a")
            .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
            .set_phase_dir(
                phase_dir=PhaseDirBuilder()
                .set_ra(ra=[123, 0.1])
                .set_dec(dec=[123, 0.1])
                .set_reference_time(reference_time="...")
                .set_reference_frame(reference_frame="ICRF3")
                .build()
            )
            .build(),
            FieldConfigurationBuilder()
            .set_field_id(field_id="field_a")
            .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
            .set_phase_dir(
                phase_dir=PhaseDirBuilder()
                .set_ra(ra=[123, 0.1])
                .set_dec(dec=[123, 0.1])
                .set_reference_time(reference_time="...")
                .set_reference_frame(reference_frame="ICRF3")
                .build()
            )
            .build(),
            True,
        ),
        (  # not_equal
            FieldConfigurationBuilder()
            .set_field_id(field_id="field_a")
            .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
            .set_phase_dir(
                phase_dir=PhaseDirBuilder()
                .set_ra(ra=[123, 0.1])
                .set_dec(dec=[123, 0.1])
                .set_reference_time(reference_time="...")
                .set_reference_frame(reference_frame="ICRF3")
                .build()
            )
            .build(),
            FieldConfigurationBuilder()
            .set_field_id(field_id="field_b")  # different field value
            .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
            .set_phase_dir(
                phase_dir=PhaseDirBuilder()
                .set_ra(ra=[123, 0.1])
                .set_dec(dec=[123, 0.1])
                .set_reference_time(reference_time="...")
                .set_reference_frame(reference_frame="ICRF3")
                .build()
            )
            .build(),
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
            EBScanTypeBuilder()
            .set_scan_type_id(scan_type_id="science")
            .set_beams(beams={"vis0": {"field_id": "field_a"}})
            .set_derive_from(derive_from=".default")
            .build(),
            EBScanTypeBuilder()
            .set_scan_type_id(scan_type_id="science")
            .set_beams(beams={"vis0": {"field_id": "field_a"}})
            .set_derive_from(derive_from=".default")
            .build(),
            True,
        ),
        (  # not_equal
            EBScanTypeBuilder()
            .set_scan_type_id(scan_type_id="science")
            .set_beams(beams={"vis0": {"field_id": "field_a"}})
            .set_derive_from(derive_from=".default")
            .build(),
            EBScanTypeBuilder()
            .set_scan_type_id(scan_type_id="science")
            .set_beams(
                beams={"vis0": {"field_id": "field_b"}}
            )  # different beam field_id
            .set_derive_from(derive_from=".default")
            .build(),
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
            EBScanTypeBeamBuilder()
            .set_field_id(field_id="pss_field_1")
            .set_channels_id(channels_id="pulsar_channels")
            .set_polarisations_id(polarisations_id="all")
            .build(),
            EBScanTypeBeamBuilder()
            .set_field_id(field_id="pss_field_1")
            .set_channels_id(channels_id="pulsar_channels")
            .set_polarisations_id(polarisations_id="all")
            .build(),
            True,
        ),
        (  # not_equal
            EBScanTypeBeamBuilder()
            .set_field_id(field_id="pss_field_1")
            .set_channels_id(channels_id="pulsar_channels")
            .set_polarisations_id(polarisations_id="all")
            .build(),
            EBScanTypeBeamBuilder()
            .set_field_id(field_id="pss_field_2")  # different field_id
            .set_channels_id(channels_id="pulsar_channels")
            .set_polarisations_id(polarisations_id="all")
            .build(),
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
            ScriptConfigurationBuilder()
            .set_kind(kind="realtime")
            .set_name(name="test-receive-addresses")
            .set_version(version="0.5.0")
            .build(),
            ScriptConfigurationBuilder()
            .set_kind(kind="realtime")
            .set_name(name="test-receive-addresses")
            .set_version(version="0.5.0")
            .build(),
            True,
        ),
        (  # not_equal
            ScriptConfigurationBuilder()
            .set_kind(kind="realtime")
            .set_name(name="test-receive-addresses")
            .set_version(version="0.5.0")
            .build(),
            ScriptConfigurationBuilder()
            .set_kind(kind="realtime")
            .set_name(name="test-receive-addresses")
            .set_version(version="0.6.0")  # different version
            .build(),
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


def test_processing_block_equality(processing_block_parameters):
    """
    Verify that Processing Block Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """

    pb1 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_parameters(parameters=processing_block_parameters)
        .set_sbi_ids(sbi_ids=["sbi-mvp01-20200325-00001"])
        .set_script(
            ScriptConfigurationBuilder()
            .set_kind(kind="realtime")
            .set_name(name="test-receive-addresses")
            .set_version(version="0.5.0")
            .build()
        )
        .build()
    )

    pb2 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_parameters(parameters=processing_block_parameters)
        .set_sbi_ids(sbi_ids=["sbi-mvp01-20200325-00003"])  # different sbi_id
        .set_script(
            ScriptConfigurationBuilder()
            .set_kind(kind="realtime")
            .set_name(name="test-receive-addresses")
            .set_version(version="0.5.0")
            .build()
        )
        .build()
    )

    assert pb1 == copy.deepcopy(pb1)
    assert pb1 != pb2
    assert pb1 != object()


def test_execution_block_configuration_equals(
    channels,
    eb_scan_type,
    beams,
    polarisation_config,
    field_config,
):
    """
    Verify that Execution Block Configuration objects are considered equal if attributes have same value and not equal if they differ.
    """

    execution_block1 = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=3600)
        .set_beams(beams=[beams])
        .set_channels(channels=[channels])
        .set_polarisations(polarisations=[polarisation_config])
        .set_fields(fields=[field_config])
        .set_scan_types(scan_types=[eb_scan_type])
        .build()
    )

    execution_block2 = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=3400)  # different max_length
        .set_beams(beams=[beams])
        .set_channels(channels=[channels])
        .set_polarisations(polarisations=[polarisation_config])
        .set_fields(fields=[field_config])
        .set_scan_types(scan_types=[eb_scan_type])
        .build()
    )

    assert execution_block1 == copy.deepcopy(execution_block1)
    assert execution_block1 != execution_block2
    assert execution_block1 != object()

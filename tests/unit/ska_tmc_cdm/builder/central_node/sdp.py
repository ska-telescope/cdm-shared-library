import functools
from typing import List

from ska_tmc_cdm.messages.central_node.sdp import (
    BeamConfiguration,
    Channel,
    ChannelConfiguration,
    EBScanType,
    EBScanTypeBeam,
    ExecutionBlockConfiguration,
    FieldConfiguration,
    PbDependency,
    PhaseDir,
    PolarisationConfiguration,
    ProcessingBlockConfiguration,
    ScanType,
    ScriptConfiguration,
    SDPConfiguration,
    SDPWorkflow,
)

ChannelBuilder = functools.partial(
    Channel,
    count=744,
    start=0,
    stride=2,
    freq_min=0.35e9,
    freq_max=1.05e9,
    link_map=((0, 0), (200, 1), (744, 2), (944, 3)),
    spectral_window_id="fsp_2_channels",
)

ScanTypeBuilder = functools.partial(
    ScanType,
    scan_type_id="science_A",
    reference_frame="ICRS",
    ra="02:42:40.771",
    dec="-00:00:47.84",
    # Note: immutable tuple to make it harder for
    # tests to interfere with each other.
    channels=(ChannelBuilder(),),
)

SDPWorkflowBuilder = functools.partial(
    SDPWorkflow, name="vis_receive", kind="realtime", version="0.1.1"
)


PbDependencyBuilder = functools.partial(
    PbDependency,
    pb_id="pb-mvp01-20200325-00001",
    kind=("visibilities",),  # tuple for test isolation
)

ScriptConfigurationBuilder = functools.partial(
    ScriptConfiguration,
    name="test-receive-addresses",
    kind="realtime",
    version="0.5.0",
)


ProcessingBlockConfigurationBuilder = functools.partial(
    ProcessingBlockConfiguration,
    pb_id="pb-mvp01-20200325-00001",
    workflow=SDPWorkflowBuilder(),
    parameters={
        "plasmaEnabled": True,
        "reception": {
            "layout": "http://127.0.0.1:80/model/default/ska1_low/layout",
            "num_channels": 13824,
            "channels_per_stream": 6912,
            "continuous_mode": True,
            "transport_protocol": "tcp",
        },
        "pvc": {"name": "receive-data"},
        "plasma_parameters": {
            "initContainers": [
                {
                    "name": "existing-output-remover",
                    "image": "artefact.skao.int/ska-sdp-realtime-receive-modules:3.3.0",
                    "command": ["rm", "-rf", "/mnt/data/output*.ms"],
                    "volumeMounts": [
                        {"mountPath": "/mnt/data", "name": "receive-data"}
                    ],
                }
            ],
            "extraContainers": [
                {
                    "name": "plasma-processor",
                    "image": "artefact.skao.int/ska-sdp-realtime-receive-modules:3.3.0",
                    "command": [
                        "plasma-mswriter",
                        "-s",
                        "/plasma/socket",
                        "--max_payloads",
                        "12",
                        "--use_plasmastman",
                        "False",
                        "/mnt/data/output.ms",
                    ],
                    "volumeMounts": [
                        {
                            "name": "plasma-storage-volume",
                            "mountPath": "/plasma",
                        },
                        {"mountPath": "/mnt/data", "name": "receive-data"},
                    ],
                },
                {
                    "name": "tmlite-server",
                    "image": "artefact.skao.int/ska-sdp-tmlite-server:0.3.0",
                },
            ],
        },
    },
)

BeamConfigurationBuilder = functools.partial(
    BeamConfiguration,
    beam_id="vis0",
    function="visibilities",
)


ChannelConfigurationBuilder = functools.partial(
    ChannelConfiguration,
    channels_id="vis_channels",
    spectral_windows=(ChannelBuilder(),),
)


PolarisationConfigurationBuilder = functools.partial(
    PolarisationConfiguration,
    polarisations_id="all",
    corr_type=("XX", "XY", "YY", "YX"),
)

PhaseDirBuilder = functools.partial(
    PhaseDir,
    ra=(123, 0.1),
    dec=(123, 0.1),
    reference_time="...",
    reference_frame="ICRF3",
)


FieldConfigurationBuilder = functools.partial(
    FieldConfiguration,
    field_id="field_a",
    pointing_fqdn="low-tmc/telstate/0/pointing",
    phase_dir=PhaseDirBuilder(),
)

EBScanTypeBuilder = functools.partial(
    EBScanType,
    scan_type_id="science",
    beams={"vis0": {"field_id": "field_a"}},
    derive_from=".default",
)

EBScanTypeBeamBuilder = functools.partial(
    EBScanTypeBeam,
    field_id="pss_field_1",
    channels_id="pulsar_channels",
    polarisations_id="all",
)


ExecutionBlockConfigurationBuilder = functools.partial(
    ExecutionBlockConfiguration,
    eb_id="eb-mvp01-20200325-00001",
    max_length=3600,
    beams=(BeamConfigurationBuilder(),),
    channels=(ChannelConfigurationBuilder(),),
    polarisations=(PolarisationConfigurationBuilder(),),
    fields=(FieldConfigurationBuilder(),),
    scan_types=(EBScanTypeBuilder(),),
)

SDPConfigurationBuilder = functools.partial(
    SDPConfiguration,
    eb_id="sbi-mvp01-20200325-00001",
    max_length=100.0,
    scan_types=(ScanTypeBuilder(),),
    processing_blocks=(ProcessingBlockConfigurationBuilder(),),
    execution_block=ExecutionBlockConfigurationBuilder(),
)

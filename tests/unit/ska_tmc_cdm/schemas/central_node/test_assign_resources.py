"""
Unit tests for ska_tmc_cdm.schemas module.
"""
import pytest
from ska_telmodel.telvalidation.semantic_validator import SchematicValidationError

from ska_tmc_cdm.messages.central_node.assign_resources import (
    AssignResourcesRequest,
    AssignResourcesResponse,
)
from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.csp import (
    CommonConfiguration,
    CSPConfiguration,
    LowCbfConfiguration,
    ResourceConfiguration,
)
from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate
from ska_tmc_cdm.messages.central_node.sdp import (
    BeamConfiguration,
    Channel,
    ChannelConfiguration,
    EBScanType,
    EBScanTypeBeam,
    ExecutionBlockConfiguration,
    FieldConfiguration,
    PbDependency,
    PolarisationConfiguration,
    ProcessingBlockConfiguration,
    ScanType,
    ScriptConfiguration,
    SDPConfiguration,
    SDPWorkflow,
)
from ska_tmc_cdm.schemas.central_node.assign_resources import (
    AssignResourcesRequestSchema,
    AssignResourcesResponseSchema,
)
from ska_tmc_cdm.schemas.central_node.sdp import SDPConfigurationSchema

from .. import utils

COMPLIANT_MID_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
    transaction_id="txn-....-00001",
    subarray_id=1,
    dish_allocation=DishAllocation(receptor_ids=["0001"]),
    sdp_config=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-assignres/0.4",
        execution_block=ExecutionBlockConfiguration(
            eb_id="eb-mvp01-20210623-00000",
            max_length=100.0,
            context={},
            beams=[
                BeamConfiguration(beam_id="vis0", function="visibilities"),
            ],
            scan_types=[
                EBScanType(
                    scan_type_id=".default",
                    beams={
                        "vis0": EBScanTypeBeam(
                            channels_id="vis_channels",
                            polarisations_id="all",
                        ),
                    },
                ),
                EBScanType(
                    scan_type_id="target:a",
                    derive_from=".default",
                    beams={"vis0": EBScanTypeBeam(field_id="field_a")},
                ),
            ],
            channels=[
                ChannelConfiguration(
                    channels_id="vis_channels",
                    spectral_windows=[
                        Channel(
                            spectral_window_id="fsp_1_channels",
                            count=14880,
                            start=0,
                            stride=2,
                            freq_min=350000000.0,
                            freq_max=368000000.0,
                            link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
                        ),
                    ],
                )
            ],
            polarisations=[
                PolarisationConfiguration(
                    polarisations_id="all",
                    corr_type=["XX", "XY", "YY", "YX"],
                )
            ],
            fields=[
                FieldConfiguration(
                    field_id="field_a",
                    phase_dir={
                        "ra": [123, 0.1],
                        "dec": [80, 0.1],
                        "reference_time": "...",
                        "reference_frame": "ICRF3",
                    },
                    pointing_fqdn="low-tmc/telstate/0/pointing",
                )
            ],
        ),
        processing_blocks=[
            ProcessingBlockConfiguration(
                pb_id="pb-mvp01-20210623-00000",
                sbi_ids=["sbi-mvp01-20200325-00001"],
                script=ScriptConfiguration(
                    kind="realtime",
                    name="vis_receive",
                    version="0.1.0",
                ),
                parameters={},
            ),
            ProcessingBlockConfiguration(
                pb_id="pb-mvp01-20210623-00001",
                sbi_ids=["sbi-mvp01-20200325-00001"],
                script=ScriptConfiguration(
                    kind="realtime",
                    name="test_realtime",
                    version="0.1.0",
                ),
                parameters={},
            ),
            ProcessingBlockConfiguration(
                pb_id="pb-mvp01-20210623-00002",
                sbi_ids=["sbi-mvp01-20200325-00002"],
                script=ScriptConfiguration(
                    kind="batch",
                    name="ical",
                    version="0.1.0",
                ),
                parameters={},
                dependencies=[
                    PbDependency(
                        pb_id="pb-mvp01-20210623-00000",
                        kind=["visibilities"],
                    )
                ],
            ),
            ProcessingBlockConfiguration(
                pb_id="pb-mvp01-20210623-00003",
                sbi_ids=[
                    "sbi-mvp01-20200325-00001",
                    "sbi-mvp01-20200325-00002",
                ],
                script=ScriptConfiguration(
                    kind="batch",
                    name="dpreb",
                    version="0.1.0",
                ),
                parameters={},
                dependencies=[
                    PbDependency(
                        pb_id="pb-mvp01-20210623-00002",
                        kind=["calibration"],
                    )
                ],
            ),
        ],
        resources={
            "csp_links": [1, 2, 3, 4],
            "receptors": ["0001"],
            "receive_nodes": 10,
        },
    ),
)


COMPLIANT_MID_ASSIGNRESOURCESREQUEST_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
  "transaction_id":"txn-....-00001",
  "subarray_id": 1,
  "dish": {"receptor_ids": ["0001"]},
  "sdp": {
      "interface":"https://schema.skao.int/ska-sdp-assignres/0.4",
      "execution_block":{
         "eb_id":"eb-mvp01-20210623-00000",
         "max_length":100.0,
         "context":{
         },
         "beams":[
            {
               "beam_id":"vis0",
               "function":"visibilities"
            }
         ],
         "scan_types":[
            {
               "scan_type_id":".default",
               "beams":{
                  "vis0":{
                     "channels_id":"vis_channels",
                     "polarisations_id":"all"
                  }
               }
            },
            {
               "scan_type_id":"target:a",
               "derive_from":".default",
               "beams":{
                  "vis0":{
                     "field_id":"field_a"
                  }
               }
            }
         ],
         "channels":[
            {
               "channels_id":"vis_channels",
               "spectral_windows":[
                  {
                     "spectral_window_id":"fsp_1_channels",
                     "count":14880,
                     "start":0,
                     "stride":2,
                     "freq_min":350000000.0,
                     "freq_max":368000000.0,
                     "link_map":[
                        [
                           0,
                           0
                        ],
                        [
                           200,
                           1
                        ],
                        [
                           744,
                           2
                        ],
                        [
                           944,
                           3
                        ]
                     ]
                  }
               ]
            }
         ],
         "polarisations":[
            {
               "polarisations_id":"all",
               "corr_type":[
                  "XX",
                  "XY",
                  "YY",
                  "YX"
               ]
            }
         ],
         "fields":[
            {
               "field_id":"field_a",
               "phase_dir":{
                  "ra":[
                     123,
                     0.1
                  ],
                  "dec":[
                     80,
                     0.1
                  ],
                  "reference_time":"...",
                  "reference_frame":"ICRF3"
               },
               "pointing_fqdn":"low-tmc/telstate/0/pointing"
            }
         ]
      },
      "processing_blocks":[
         {
            "pb_id":"pb-mvp01-20210623-00000",
            "sbi_ids":[
               "sbi-mvp01-20200325-00001"
            ],
            "script":{
               "kind":"realtime",
               "name":"vis_receive",
               "version":"0.1.0"
            },
            "parameters":{      
            }
         },
         {
            "pb_id":"pb-mvp01-20210623-00001",
            "sbi_ids":[
               "sbi-mvp01-20200325-00001"
            ],
            "script":{
               "kind":"realtime",
               "name":"test_realtime",
               "version":"0.1.0"
            },
            "parameters":{       
            }
         },
         {
            "pb_id":"pb-mvp01-20210623-00002",
            "sbi_ids":[
               "sbi-mvp01-20200325-00002"
            ],
            "script":{
               "kind":"batch",
               "name":"ical",
               "version":"0.1.0"
            },
            "parameters":{
            },
            "dependencies":[
               {
                  "pb_id":"pb-mvp01-20210623-00000",
                  "kind":[
                     "visibilities"
                  ]
               }
            ]
         },
         {
            "pb_id":"pb-mvp01-20210623-00003",
            "sbi_ids":[
               "sbi-mvp01-20200325-00001",
               "sbi-mvp01-20200325-00002"
            ],
            "script":{
               "kind":"batch",
               "name":"dpreb",
               "version":"0.1.0"
            },
            "parameters":{  
            },
            "dependencies":[
               {
                  "pb_id":"pb-mvp01-20210623-00002",
                  "kind":[
                     "calibration"
                  ]
               }
            ]
         }
      ],
      "resources":{
         "csp_links":[
            1,
            2,
            3,
            4
         ],
         "receptors":[
            "0001"
         ],
         "receive_nodes":10
        }
    }
}
"""
VALID_MID_ASSIGNRESOURCESREQUEST_COMPLIANT_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
    "transaction_id": "txn-....-00001",
    "subarray_id": 1,
    "dish": {
        "receptor_ids": ["0001"]
    },
    "sdp": {
        "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
        "execution_block": {
            "eb_id": "eb-mvp01-20210623-00000",
            "max_length": 100.0,
            "context": {},
            "beams": [{
                "beam_id": "vis0",
                "function": "visibilities"
            }],
            "scan_types": [{
                "scan_type_id": ".default",
                "beams": {
                    "vis0": {
                        "channels_id": "vis_channels",
                        "polarisations_id": "all"
                    },
                    "pss1": {
                        "field_id": "pss_field_0",
                        "channels_id": "pulsar_channels",
                        "polarisations_id": "all"
                    },
                    "pss2": {
                        "field_id": "pss_field_1",
                        "channels_id": "pulsar_channels",
                        "polarisations_id": "all"
                    },
                    "pst1": {
                        "field_id": "pst_field_0",
                        "channels_id": "pulsar_channels",
                        "polarisations_id": "all"
                    },
                    "pst2": {
                        "field_id": "pst_field_1",
                        "channels_id": "pulsar_channels",
                        "polarisations_id": "all"
                    },
                    "vlbi": {
                        "field_id": "vlbi_field",
                        "channels_id": "vlbi_channels",
                        "polarisations_id": "all"
                    }
                }
            }, {
                "scan_type_id": "target:a",
                "derive_from": ".default",
                "beams": {
                    "vis0": {
                        "field_id": "field_a"
                    }
                }
            }],
            "channels": [{
                "channels_id": "vis_channels",
                "spectral_windows": [{
                    "spectral_window_id": "fsp_1_channels",
                    "count": 14880,
                    "start": 0,
                    "stride": 2,
                    "freq_min": 350000000.0,
                    "freq_max": 368000000.0,
                    "link_map": [
                        [0, 0],
                        [200, 1],
                        [744, 2],
                        [944, 3]
                    ]
                }]
            }, {
                "channels_id": "pulsar_channels",
                "spectral_windows": [{
                    "spectral_window_id": "pulsar_fsp_channels",
                    "count": 14880,
                    "start": 0,
                    "freq_min": 350000000.0,
                    "freq_max": 368000000.0
                }]
            }],
            "polarisations": [{
                "polarisations_id": "all",
                "corr_type": ["XX", "XY", "YY", "YX"]
            }],
            "fields": [{
                "field_id": "field_a",
                "phase_dir": {
                    "ra": [123, 0.1],
                    "dec": [80, 0.1],
                    "reference_time": "...",
                    "reference_frame": "ICRF3"
                },
                "pointing_fqdn": "low-tmc/telstate/0/pointing"
            }]
        },
        "processing_blocks": [{
            "pb_id": "pb-mvp01-20210623-00000",
            "sbi_ids": ["sbi-mvp01-20200325-00001"],
            "script": {
                "kind": "realtime",
                "name": "vis_receive",
                "version": "0.1.0"
            },
            "parameters": {}
        }, {
            "pb_id": "pb-mvp01-20210623-00001",
            "sbi_ids": ["sbi-mvp01-20200325-00001"],
            "script": {
                "kind": "realtime",
                "name": "test_realtime",
                "version": "0.1.0"
            },
            "parameters": {}
        }, {
            "pb_id": "pb-mvp01-20210623-00002",
            "sbi_ids": ["sbi-mvp01-20200325-00002"],
            "script": {
                "kind": "batch",
                "name": "ical",
                "version": "0.1.0"
            },
            "parameters": {},
            "dependencies": [{
                "pb_id": "pb-mvp01-20210623-00000",
                "kind": ["visibilities"]
            }]
        }, {
            "pb_id": "pb-mvp01-20210623-00003",
            "sbi_ids": ["sbi-mvp01-20200325-00001", "sbi-mvp01-20200325-00002"],
            "script": {
                "kind": "batch",
                "name": "dpreb",
                "version": "0.1.0"
            },
            "parameters": {},
            "dependencies": [{
                "pb_id": "pb-mvp01-20210623-00002",
                "kind": ["calibration"]
            }]
        }],
        "resources": {
            "csp_links": [1, 2, 3, 4],
            "receptors": ["0001"],
            "receive_nodes": 10
        }
    }
}
"""
VALID_SDP_COMPLIANT_OBJECT = SDPConfiguration(
    interface="https://schema.skao.int/ska-sdp-assignres/0.4",
    execution_block=ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20210623-00000",
        max_length=100.0,
        context={},
        beams=[
            BeamConfiguration(beam_id="vis0", function="visibilities"),
        ],
        scan_types=[
            EBScanType(
                scan_type_id=".default",
                beams={
                    "vis0": EBScanTypeBeam(
                        channels_id="vis_channels",
                        polarisations_id="all",
                    ),
                    "pss1": EBScanTypeBeam(
                        field_id="pss_field_0",
                        channels_id="pulsar_channels",
                        polarisations_id="all",
                    ),
                    "pss2": EBScanTypeBeam(
                        field_id="pss_field_1",
                        channels_id="pulsar_channels",
                        polarisations_id="all",
                    ),
                    "pst1": EBScanTypeBeam(
                        field_id="pst_field_0",
                        channels_id="pulsar_channels",
                        polarisations_id="all",
                    ),
                    "pst2": EBScanTypeBeam(
                        field_id="pst_field_1",
                        channels_id="pulsar_channels",
                        polarisations_id="all",
                    ),
                    "vlbi": EBScanTypeBeam(
                        field_id="vlbi_field",
                        channels_id="vlbi_channels",
                        polarisations_id="all",
                    ),
                },
            ),
            EBScanType(
                scan_type_id="target:a",
                derive_from=".default",
                beams={"vis0": EBScanTypeBeam(field_id="field_a")},
            ),
        ],
        channels=[
            ChannelConfiguration(
                channels_id="vis_channels",
                spectral_windows=[
                    Channel(
                        spectral_window_id="fsp_1_channels",
                        count=14880,
                        start=0,
                        stride=2,
                        freq_min=350000000.0,
                        freq_max=368000000.0,
                        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
                    ),
                ],
            )
        ],
        polarisations=[
            PolarisationConfiguration(
                polarisations_id="all",
                corr_type=["XX", "XY", "YY", "YX"],
            )
        ],
        fields=[
            FieldConfiguration(
                field_id="field_a",
                phase_dir={
                    "ra": [123, 0.1],
                    "dec": [80, 0.1],
                    "reference_time": "...",
                    "reference_frame": "ICRF3",
                },
                pointing_fqdn="low-tmc/telstate/0/pointing",
            )
        ],
    ),
    processing_blocks=[
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20210623-00000",
            sbi_ids=["sbi-mvp01-20200325-00001"],
            script=ScriptConfiguration(
                kind="realtime",
                name="vis_receive",
                version="0.1.0",
            ),
            parameters={},
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20210623-00001",
            sbi_ids=["sbi-mvp01-20200325-00001"],
            script=ScriptConfiguration(
                kind="realtime",
                name="test_realtime",
                version="0.1.0",
            ),
            parameters={},
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20210623-00002",
            sbi_ids=["sbi-mvp01-20200325-00002"],
            script=ScriptConfiguration(
                kind="batch",
                name="ical",
                version="0.1.0",
            ),
            parameters={},
            dependencies=[
                PbDependency(
                    pb_id="pb-mvp01-20210623-00000",
                    kind=["visibilities"],
                )
            ],
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20210623-00003",
            sbi_ids=[
                "sbi-mvp01-20200325-00001",
                "sbi-mvp01-20200325-00002",
            ],
            script=ScriptConfiguration(
                kind="batch",
                name="dpreb",
                version="0.1.0",
            ),
            parameters={},
            dependencies=[
                PbDependency(
                    pb_id="pb-mvp01-20210623-00002",
                    kind=["calibration"],
                )
            ],
        ),
    ],
    resources={
        "csp_links": [1, 2, 3, 4],
        "receptors": ["0001"],
        "receive_nodes": 10,
    },
)


VALID_MID_ASSIGNRESOURCESREQUEST_COMPLIANT_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
    transaction_id="txn-mvp01-20200325-00004",
    subarray_id=1,
    dish_allocation=DishAllocation(receptor_ids=["0001"]),
    sdp_config=VALID_SDP_COMPLIANT_OBJECT,
)

VALID_SDP_JSON = """{
  "interface": "https://schema.skao.int/ska-sdp-assignresources/2.0",
  "eb_id": "eb-mvp01-20200325-00001",
  "max_length": 100.0,
  "scan_types": [
    {
      "scan_type_id": "science_A",
      "reference_frame": "ICRS",
      "ra": "02:42:40.771",
      "dec": "-00:00:47.84",
      "channels": [
        {
          "count": 744,
          "start": 0,
          "stride": 2,
          "freq_min": 0.35e9,
          "freq_max": 0.368e9,
          "link_map": [[0, 0], [200, 1], [744, 2], [944, 3]]
        },
        {
          "count": 744,
          "start": 2000,
          "stride": 1,
          "freq_min": 0.36e9,
          "freq_max": 0.368e9,
          "link_map": [[2000, 4], [2200, 5]]
        }
      ]
    },
    {
      "scan_type_id": "calibration_B",
      "reference_frame": "ICRS",
      "ra": "12:29:06.699",
      "dec": "02:03:08.598",
      "channels": [
        {
          "count": 744,
          "start": 0,
          "stride": 2,
          "freq_min": 0.35e9,
          "freq_max": 0.368e9,
          "link_map": [[0, 0], [200, 1], [744, 2], [944, 3]]
        },
        {
          "count": 744,
          "start": 2000,
          "stride": 1,
          "freq_min": 0.36e9,
          "freq_max": 0.368e9,
          "link_map": [[2000, 4], [2200, 5]]
        }
      ]
    }
  ],
  "processing_blocks": [
    {
      "pb_id": "pb-mvp01-20200325-00001",
      "workflow": {
        "kind": "realtime",
        "name": "vis_receive",
        "version": "0.1.0"
      },
      "parameters": {}
    },
    {
      "pb_id": "pb-mvp01-20200325-00002",
      "workflow": {
        "kind": "realtime",
        "name": "test_realtime",
        "version": "0.1.0"
      },
      "parameters": {}
    },
    {
      "pb_id": "pb-mvp01-20200325-00003",
      "workflow": {"kind": "batch", "name": "ical", "version": "0.1.0"},
      "parameters": {},
      "dependencies": [
        {"pb_id": "pb-mvp01-20200325-00001", "kind": ["visibilities"]}
      ]
    },
    {
      "pb_id": "pb-mvp01-20200325-00004",
      "workflow": {"kind": "batch", "name": "dpreb", "version": "0.1.0"},
      "parameters": {},
      "dependencies": [
        {"pb_id": "pb-mvp01-20200325-00003", "kind": ["calibration"]}
      ]
    }
  ]
}"""

VALID_SDP_OBJECT = SDPConfiguration(
    interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    eb_id="eb-mvp01-20200325-00001",
    max_length=100.0,
    scan_types=[
        ScanType(
            "science_A",
            "ICRS",
            "02:42:40.771",
            "-00:00:47.84",
            [
                Channel(
                    744, 0, 2, 0.35e9, 0.368e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
                ),
                Channel(744, 2000, 1, 0.36e9, 0.368e9, [[2000, 4], [2200, 5]]),
            ],
        ),
        ScanType(
            "calibration_B",
            "ICRS",
            "12:29:06.699",
            "02:03:08.598",
            [
                Channel(
                    744, 0, 2, 0.35e9, 0.368e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
                ),
                Channel(744, 2000, 1, 0.36e9, 0.368e9, [[2000, 4], [2200, 5]]),
            ],
        ),
    ],
    processing_blocks=[
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20200325-00001",
            workflow=SDPWorkflow("vis_receive", "realtime", "0.1.0"),
            parameters={},
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20200325-00002",
            workflow=SDPWorkflow("test_realtime", "realtime", "0.1.0"),
            parameters={},
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20200325-00003",
            workflow=SDPWorkflow("ical", "batch", "0.1.0"),
            parameters={},
            dependencies=[PbDependency("pb-mvp01-20200325-00001", ["visibilities"])],
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20200325-00004",
            workflow=SDPWorkflow("dpreb", "batch", "0.1.0"),
            parameters={},
            dependencies=[PbDependency("pb-mvp01-20200325-00003", ["calibration"])],
        ),
    ],
)

VALID_MID_ASSIGNRESOURCESREQUEST_JSON = (
    """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.0",
  "transaction_id":"txn-mvp01-20200325-00004",
  "subarray_id": 1,
  "dish": {"receptor_ids": ["0001", "0002"]},
  "sdp": """
    + VALID_SDP_JSON
    + """
}
"""
)

VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
    transaction_id="txn-mvp01-20200325-00004",
    subarray_id=1,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"]),
    sdp_config=VALID_SDP_OBJECT,
)

VALID_LOW_ASSIGNRESOURCESREQUEST_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-tmc-assignresources/2.0",
  "transaction_id":"txn-mvp01-20200325-00004",
  "subarray_id": 1,
  "mccs": {
    "subarray_beam_ids": [1],
    "station_ids": [[1, 2]],
    "channel_blocks": [1, 2, 3, 4, 5]
  }
}
"""

VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-assignresources/2.0",
    transaction_id="txn-mvp01-20200325-00004",
    subarray_id=1,
    mccs=MCCSAllocate(
        subarray_beam_ids=[1], station_ids=[(1, 2)], channel_blocks=[1, 2, 3, 4, 5]
    ),
)

INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON = """{
  "interface": "https://schema.skao.int/ska-low-tmc-assignresources/999999.0",
  "subarray_id": 1,
  "mccs": {
    "subarray_beam_ids": [1, 2, 3],
    "station_ids": [[1, 2]],
    "channel_blocks": [1, 2, 3, 4, 5]
  }
}"""

VALID_MID_ASSIGNRESOURCESRESPONSE_JSON = """
{
    "dish": {"receptor_ids_allocated": ["0001", "0002"]}
}
"""

VALID_MID_ASSIGNRESOURCESRESPONSE_OBJECT = AssignResourcesResponse(
    dish_allocation=DishAllocation(["0001", "0002"])
)

VALID_SDP_JSON_PI16 = """
{
      "interface":"https://schema.skao.int/ska-sdp-assignres/0.4",
      "execution_block":{
         "eb_id":"eb-mvp01-20210623-00000",
         "max_length":100.0,
         "context":{
         },
         "beams":[
            {
               "beam_id":"vis0",
               "function":"visibilities"
            },
            {
               "beam_id":"pss1",
               "search_beam_id":1,
               "function":"pulsar search"
            },
            {
               "beam_id":"pss2",
               "search_beam_id":2,
               "function":"pulsar search"
            },
            {
               "beam_id":"pst1",
               "timing_beam_id":1,
               "function":"pulsar timing"
            },
            {
               "beam_id":"pst2",
               "timing_beam_id":2,
               "function":"pulsar timing"
            },
            {
               "beam_id":"vlbi1",
               "vlbi_beam_id":1,
               "function":"vlbi"
            }
         ],
         "scan_types":[
            {
               "scan_type_id":".default",
               "beams":{
                  "vis0":{
                     "channels_id":"vis_channels",
                     "polarisations_id":"all"
                  },
                  "pss1":{
                     "field_id":"pss_field_0",
                     "channels_id":"pulsar_channels",
                     "polarisations_id":"all"
                  },
                  "pss2":{
                     "field_id":"pss_field_1",
                     "channels_id":"pulsar_channels",
                     "polarisations_id":"all"
                  },
                  "pst1":{
                     "field_id":"pst_field_0",
                     "channels_id":"pulsar_channels",
                     "polarisations_id":"all"
                  },
                  "pst2":{
                     "field_id":"pst_field_1",
                     "channels_id":"pulsar_channels",
                     "polarisations_id":"all"
                  },
                  "vlbi":{
                     "field_id":"vlbi_field",
                     "channels_id":"vlbi_channels",
                     "polarisations_id":"all"
                  }
               }
            },
            {
               "scan_type_id":"target:a",
               "derive_from":".default",
               "beams":{
                  "vis0":{
                     "field_id":"field_a"
                  }
               }
            }
         ],
         "channels":[
            {
               "channels_id":"vis_channels",
               "spectral_windows":[
                  {
                     "spectral_window_id":"fsp_1_channels",
                     "count":744,
                     "start":0,
                     "stride":2,
                     "freq_min":350000000.0,
                     "freq_max":368000000.0,
                     "link_map":[
                        [
                           0,
                           0
                        ],
                        [
                           200,
                           1
                        ],
                        [
                           744,
                           2
                        ],
                        [
                           944,
                           3
                        ]
                     ]
                  },
                  {
                     "spectral_window_id":"fsp_2_channels",
                     "count":744,
                     "start":2000,
                     "stride":1,
                     "freq_min":360000000.0,
                     "freq_max":368000000.0,
                     "link_map":[
                        [
                           2000,
                           4
                        ],
                        [
                           2200,
                           5
                        ]
                     ]
                  },
                  {
                     "spectral_window_id":"zoom_window_1",
                     "count":744,
                     "start":4000,
                     "stride":1,
                     "freq_min":360000000.0,
                     "freq_max":361000000.0,
                     "link_map":[
                        [
                           4000,
                           6
                        ],
                        [
                           4200,
                           7
                        ]
                     ]
                  }
               ]
            }
         ],
         "polarisations":[
            {
               "polarisations_id":"all",
               "corr_type":[
                  "XX",
                  "XY",
                  "YY",
                  "YX"
               ]
            }
         ],
         "fields":[
            {
               "field_id":"field_a",
               "phase_dir":{
                  "ra":[
                     123,
                     0.1
                  ],
                  "dec":[
                     80,
                     0.1
                  ],
                  "reference_time":"...",
                  "reference_frame":"ICRF3"
               },
               "pointing_fqdn":"low-tmc/telstate/0/pointing"
            }
         ]
      },
      "processing_blocks":[
         {
            "pb_id":"pb-mvp01-20210623-00000",
            "sbi_ids":[
               "sbi-mvp01-20200325-00001"
            ],
            "script":{
               "kind":"realtime",
               "name":"vis_receive",
               "version":"0.1.0"
            },
            "parameters":{      
            }
         },
         {
            "pb_id":"pb-mvp01-20210623-00001",
            "sbi_ids":[
               "sbi-mvp01-20200325-00001"
            ],
            "script":{
               "kind":"realtime",
               "name":"test_realtime",
               "version":"0.1.0"
            },
            "parameters":{       
            }
         },
         {
            "pb_id":"pb-mvp01-20210623-00002",
            "sbi_ids":[
               "sbi-mvp01-20200325-00002"
            ],
            "script":{
               "kind":"batch",
               "name":"ical",
               "version":"0.1.0"
            },
            "parameters":{
            },
            "dependencies":[
               {
                  "pb_id":"pb-mvp01-20210623-00000",
                  "kind":[
                     "visibilities"
                  ]
               }
            ]
         },
         {
            "pb_id":"pb-mvp01-20210623-00003",
            "sbi_ids":[
               "sbi-mvp01-20200325-00001",
               "sbi-mvp01-20200325-00002"
            ],
            "script":{
               "kind":"batch",
               "name":"dpreb",
               "version":"0.1.0"
            },
            "parameters":{  
            },
            "dependencies":[
               {
                  "pb_id":"pb-mvp01-20210623-00002",
                  "kind":[
                     "calibration"
                  ]
               }
            ]
         }
      ],
      "resources":{
         "csp_links":[
            1,
            2,
            3,
            4
         ],
         "receptors":[
            "FS4",
            "FS8",
            "FS16",
            "FS17",
            "FS22",
            "FS23",
            "FS30",
            "FS31",
            "FS32",
            "FS33",
            "FS36",
            "FS52",
            "FS56",
            "FS57",
            "FS59",
            "FS62",
            "FS66",
            "FS69",
            "FS70",
            "FS72",
            "FS73",
            "FS78",
            "FS80",
            "FS88",
            "FS89",
            "FS90",
            "FS91",
            "FS98",
            "FS108",
            "FS111",
            "FS132",
            "FS144",
            "FS146",
            "FS158",
            "FS165",
            "FS167",
            "FS176",
            "FS183",
            "FS193",
            "FS200",
            "FS345",
            "FS346",
            "FS347",
            "FS348",
            "FS349",
            "FS350",
            "FS351",
            "FS352",
            "FS353",
            "FS354",
            "FS355",
            "FS356",
            "FS429",
            "FS430",
            "FS431",
            "FS432",
            "FS433",
            "FS434",
            "FS465",
            "FS466",
            "FS467",
            "FS468",
            "FS469",
            "FS470"
         ],
         "receive_nodes":10
  }
}"""

VALID_SDP_OBJECT_PI16 = SDPConfiguration(
    interface="https://schema.skao.int/ska-sdp-assignres/0.4",
    execution_block=ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20210623-00000",
        max_length=100.0,
        context={},
        beams=[
            BeamConfiguration(beam_id="vis0", function="visibilities"),
            BeamConfiguration(
                beam_id="pss1",
                search_beam_id=1,
                function="pulsar search",
            ),
            BeamConfiguration(
                beam_id="pss2",
                search_beam_id=2,
                function="pulsar search",
            ),
            BeamConfiguration(
                beam_id="pst1",
                timing_beam_id=1,
                function="pulsar timing",
            ),
            BeamConfiguration(
                beam_id="pst2",
                timing_beam_id=2,
                function="pulsar timing",
            ),
            BeamConfiguration(beam_id="vlbi1", vlbi_beam_id=1, function="vlbi"),
        ],
        scan_types=[
            EBScanType(
                scan_type_id=".default",
                beams={
                    "vis0": EBScanTypeBeam(
                        channels_id="vis_channels",
                        polarisations_id="all",
                    ),
                    "pss1": EBScanTypeBeam(
                        field_id="pss_field_0",
                        channels_id="pulsar_channels",
                        polarisations_id="all",
                    ),
                    "pss2": EBScanTypeBeam(
                        field_id="pss_field_1",
                        channels_id="pulsar_channels",
                        polarisations_id="all",
                    ),
                    "pst1": EBScanTypeBeam(
                        field_id="pst_field_0",
                        channels_id="pulsar_channels",
                        polarisations_id="all",
                    ),
                    "pst2": EBScanTypeBeam(
                        field_id="pst_field_1",
                        channels_id="pulsar_channels",
                        polarisations_id="all",
                    ),
                    "vlbi": EBScanTypeBeam(
                        field_id="vlbi_field",
                        channels_id="vlbi_channels",
                        polarisations_id="all",
                    ),
                },
            ),
            EBScanType(
                scan_type_id="target:a",
                derive_from=".default",
                beams={"vis0": EBScanTypeBeam(field_id="field_a")},
            ),
        ],
        channels=[
            ChannelConfiguration(
                channels_id="vis_channels",
                spectral_windows=[
                    Channel(
                        spectral_window_id="fsp_1_channels",
                        count=744,
                        start=0,
                        stride=2,
                        freq_min=350000000.0,
                        freq_max=368000000.0,
                        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
                    ),
                    Channel(
                        spectral_window_id="fsp_2_channels",
                        count=744,
                        start=2000,
                        stride=1,
                        freq_min=360000000.0,
                        freq_max=368000000.0,
                        link_map=[[2000, 4], [2200, 5]],
                    ),
                    Channel(
                        spectral_window_id="zoom_window_1",
                        count=744,
                        start=4000,
                        stride=1,
                        freq_min=360000000.0,
                        freq_max=361000000.0,
                        link_map=[[4000, 6], [4200, 7]],
                    ),
                ],
            )
        ],
        polarisations=[
            PolarisationConfiguration(
                polarisations_id="all",
                corr_type=["XX", "XY", "YY", "YX"],
            )
        ],
        fields=[
            FieldConfiguration(
                field_id="field_a",
                phase_dir={
                    "ra": [123, 0.1],
                    "dec": [80, 0.1],
                    "reference_time": "...",
                    "reference_frame": "ICRF3",
                },
                pointing_fqdn="low-tmc/telstate/0/pointing",
            )
        ],
    ),
    processing_blocks=[
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20210623-00000",
            sbi_ids=["sbi-mvp01-20200325-00001"],
            script=ScriptConfiguration(
                kind="realtime",
                name="vis_receive",
                version="0.1.0",
            ),
            parameters={},
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20210623-00001",
            sbi_ids=["sbi-mvp01-20200325-00001"],
            script=ScriptConfiguration(
                kind="realtime",
                name="test_realtime",
                version="0.1.0",
            ),
            parameters={},
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20210623-00002",
            sbi_ids=["sbi-mvp01-20200325-00002"],
            script=ScriptConfiguration(
                kind="batch",
                name="ical",
                version="0.1.0",
            ),
            parameters={},
            dependencies=[
                PbDependency(
                    pb_id="pb-mvp01-20210623-00000",
                    kind=["visibilities"],
                )
            ],
        ),
        ProcessingBlockConfiguration(
            pb_id="pb-mvp01-20210623-00003",
            sbi_ids=[
                "sbi-mvp01-20200325-00001",
                "sbi-mvp01-20200325-00002",
            ],
            script=ScriptConfiguration(
                kind="batch",
                name="dpreb",
                version="0.1.0",
            ),
            parameters={},
            dependencies=[
                PbDependency(
                    pb_id="pb-mvp01-20210623-00002",
                    kind=["calibration"],
                )
            ],
        ),
    ],
    resources={
        "csp_links": [1, 2, 3, 4],
        "receptors": [
            "FS4",
            "FS8",
            "FS16",
            "FS17",
            "FS22",
            "FS23",
            "FS30",
            "FS31",
            "FS32",
            "FS33",
            "FS36",
            "FS52",
            "FS56",
            "FS57",
            "FS59",
            "FS62",
            "FS66",
            "FS69",
            "FS70",
            "FS72",
            "FS73",
            "FS78",
            "FS80",
            "FS88",
            "FS89",
            "FS90",
            "FS91",
            "FS98",
            "FS108",
            "FS111",
            "FS132",
            "FS144",
            "FS146",
            "FS158",
            "FS165",
            "FS167",
            "FS176",
            "FS183",
            "FS193",
            "FS200",
            "FS345",
            "FS346",
            "FS347",
            "FS348",
            "FS349",
            "FS350",
            "FS351",
            "FS352",
            "FS353",
            "FS354",
            "FS355",
            "FS356",
            "FS429",
            "FS430",
            "FS431",
            "FS432",
            "FS433",
            "FS434",
            "FS465",
            "FS466",
            "FS467",
            "FS468",
            "FS469",
            "FS470",
        ],
        "receive_nodes": 10,
    },
)

VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16 = (
    """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
  "transaction_id":"txn-....-00001",
  "subarray_id": 1,
  "dish": {"receptor_ids": ["0001"]},
  "sdp": """
    + VALID_SDP_JSON_PI16
    + """
}
"""
)


INVALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16 = (
    """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
  "transaction_id":"txn-....-00001",
  "subarray_id": 1,
  "dish": "foo",
  "sdp": """
    + VALID_SDP_JSON_PI16
    + """
}
"""
)

VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT_PI16 = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
    transaction_id="txn-....-00001",
    subarray_id=1,
    dish_allocation=DishAllocation(receptor_ids=["0001"]),
    sdp_config=VALID_SDP_OBJECT_PI16,
)


VALID_LOW_ASSIGNRESOURCESREQUEST_JSON_PI17 = (
    """
{
  "interface": "https://schema.skao.int/ska-low-tmc-assignresources/3.0",
  "transaction_id": "txn-....-00001",
  "subarray_id": 1,
  "mccs": {
    "subarray_beam_ids": [
      1
    ],
    "station_ids": [
      [
        1,
        2
      ]
    ],
    "channel_blocks": [
      3
    ]
  },
    "sdp": """
    + VALID_SDP_JSON_PI16
    + """,
  "csp": {
    "interface": "https://schema.skao.int/ska-low-csp-assignresources/2.0",
    "common": {
      "subarray_id": 1
    },
    "lowcbf": {
      "resources": [
        {
          "device": "fsp_01",
          "shared": true,
          "fw_image": "pst",
          "fw_mode": "unused"
        },
        {
          "device": "p4_01",
          "shared": true,
          "fw_image": "p4.bin",
          "fw_mode": "p4"
        }
      ]
    }
  }
}
"""
)

VALID_LOW_CSP_OBJECT_PI17 = CSPConfiguration(
    interface="https://schema.skao.int/ska-low-csp-assignresources/2.0",
    common=CommonConfiguration(subarray_id=1),
    lowcbf=LowCbfConfiguration(
        resources=[
            ResourceConfiguration(
                device="fsp_01", shared=True, fw_image="pst", fw_mode="unused"
            ),
            ResourceConfiguration(
                device="p4_01", shared=True, fw_image="p4.bin", fw_mode="p4"
            ),
        ]
    ),
)

VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT_PI17 = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-assignresources/3.0",
    transaction_id="txn-....-00001",
    subarray_id=1,
    mccs=MCCSAllocate(subarray_beam_ids=[1], station_ids=[(1, 2)], channel_blocks=[3]),
    sdp_config=VALID_SDP_OBJECT_PI16,
    csp_config=VALID_LOW_CSP_OBJECT_PI17,
)


def low_invalidator_fn(o: AssignResourcesRequest):
    # function to make a valid LOW AssignedResourcesRequest invalid
    o.mccs.subarray_beam_ids = [1, 2, 3]


def mid_invalidator_fn(o: AssignResourcesRequest):
    # function to make a valid MID AssignResourcesRequest invalid
    o.sdp_config.max_length = 10


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json,is_validate,is_semantic_validate",
    [
        (
            AssignResourcesRequestSchema,
            VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
            low_invalidator_fn,
            VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
            INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
            True,
            False,
        ),
        (
            AssignResourcesRequestSchema,
            VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT,
            None,
            VALID_MID_ASSIGNRESOURCESREQUEST_JSON,
            None,
            False,
            False,
        ),
        (
            AssignResourcesResponseSchema,
            VALID_MID_ASSIGNRESOURCESRESPONSE_OBJECT,
            None,
            VALID_MID_ASSIGNRESOURCESRESPONSE_JSON,
            None,
            False,
            False,
        ),
        (
            SDPConfigurationSchema,
            VALID_SDP_OBJECT,
            None,
            VALID_SDP_JSON,
            None,
            True,
            False,
        ),
        (
            SDPConfigurationSchema,
            VALID_SDP_OBJECT_PI16,
            None,
            VALID_SDP_JSON_PI16,
            None,
            True,
            False,
        ),
        (
            AssignResourcesRequestSchema,
            VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT_PI17,
            None,
            VALID_LOW_ASSIGNRESOURCESREQUEST_JSON_PI17,
            None,
            False,
            False,
        ),
        (
            AssignResourcesRequestSchema,
            VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT_PI16,
            mid_invalidator_fn,
            VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16,
            INVALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16,
            True,
            False,
        ),
        (
            AssignResourcesRequestSchema,
            COMPLIANT_MID_ASSIGNRESOURCESREQUEST_OBJECT,
            None,
            COMPLIANT_MID_ASSIGNRESOURCESREQUEST_JSON,
            None,
            False,
            False,
        ),
    ],
)
def test_assignresources_serialisation_and_validation(
    schema_cls,
    instance,
    modifier_fn,
    valid_json,
    invalid_json,
    is_validate,
    is_semantic_validate,
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    # pytest raise error, assert

    if should_raise_exception(is_semantic_validate):
        with pytest.raises(SchematicValidationError):
            utils.test_schema_serialisation_and_validation(
                schema_cls,
                instance,
                modifier_fn,
                valid_json,
                invalid_json,
                is_validate,
                is_semantic_validate,
            )
    else:
        utils.test_schema_serialisation_and_validation(
            schema_cls,
            instance,
            modifier_fn,
            valid_json,
            invalid_json,
            is_validate,
            is_semantic_validate,
        )


def should_raise_exception(is_semantic_validate):
    return is_semantic_validate

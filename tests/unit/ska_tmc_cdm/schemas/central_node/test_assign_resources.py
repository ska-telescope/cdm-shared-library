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
from ska_tmc_cdm.messages.mccssubarray.scan import ScanRequest
from ska_tmc_cdm.schemas.central_node.assign_resources import (
    AssignResourcesRequestSchema,
    AssignResourcesResponseSchema,
)
from ska_tmc_cdm.schemas.central_node.sdp import SDPConfigurationSchema
from ska_tmc_cdm.schemas.mccssubarray.scan import ScanRequestSchema

from .. import utils

VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT_PI16 = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
    transaction_id="txn-....-00001",
    subarray_id=1,
    dish_allocation=DishAllocation(receptor_ids=["SKA001"]),
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
            "receptors": ["SKA001"],
            "receive_nodes": 10,
        },
    ),
)


VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16 = """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
  "transaction_id":"txn-....-00001",
  "subarray_id": 1,
  "dish": {"receptor_ids": ["SKA001"]},
  "sdp": {
      "interface":"https://schema.skao.int/ska-sdp-assignres/0.4",
      "execution_block":{
         "eb_id":"eb-mvp01-20210623-00000",
         "max_length":100.0,
         "context":{},
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
            "SKA001"
         ],
         "receive_nodes":10
        }
    }
}
"""

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
               "function":"pulsar search"
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
                     "freq_min":35000000.0,
                     "freq_max":49880000000000.0,
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
            BeamConfiguration(beam_id="vis0", function="pulsar search"),
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
                        freq_min=35000000.0,
                        freq_max=49880000000000.0,
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

VALID_SDP_JSON_PI20 = """
{
    "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
    "resources": {
      "receptors": [
        "SKA001",
        "SKA002",
        "SKA003",
        "SKA004"
      ]
    },
    "execution_block": {
      "eb_id": "eb-test-20220916-00000",
      "context": {
      },
      "max_length": 3600.0,
      "beams": [
        {
          "beam_id": "vis0",
          "function": "visibilities"
        }
      ],
      "scan_types": [
        {
          "scan_type_id": ".default",
          "beams": {
            "vis0": {
              "channels_id": "vis_channels",
              "polarisations_id": "all"
            }
          }
        },
        {
          "scan_type_id": "target:a",
          "derive_from": ".default",
          "beams": {
            "vis0": {
              "field_id": "field_a"
            }
          }
        },
        {
          "scan_type_id": "calibration:b",
          "derive_from": ".default",
          "beams": {
            "vis0": {
              "field_id": "field_b"
            }
          }
        }
      ],
      "channels": [
        {
          "channels_id": "vis_channels",
          "spectral_windows": [
            {
              "spectral_window_id": "fsp_1_channels",
              "count": 4,
              "start": 0,
              "stride": 2,
              "freq_min": 350000000.0,
              "freq_max": 368000000.0,
              "link_map": [
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
      "polarisations": [
        {
          "polarisations_id": "all",
          "corr_type": [
            "XX",
            "XY",
            "YX",
            "YY"
          ]
        }
      ],
      "fields": [
        {
          "field_id": "field_a",
          "phase_dir": {
            "ra": [
              123.0
            ],
            "dec": [
              -60.0
            ],
            "reference_time": "...",
            "reference_frame": "ICRF3"
          },
          "pointing_fqdn": "..."
        },
        {
          "field_id": "field_b",
          "phase_dir": {
            "ra": [
              123.0
            ],
            "dec": [
              -60.0
            ],
            "reference_time": "...",
            "reference_frame": "ICRF3"
          },
          "pointing_fqdn": "..."
        }
      ]
    },
    "processing_blocks": [
      {
        "pb_id": "pb-test-20220916-00000",
        "script": {
          "kind": "realtime",
          "name": "test-receive-addresses",
          "version": "0.5.0"
        },
        "sbi_ids": [
          "sbi-test-20220916-00000"
        ],
        "parameters": {}
      }
    ]
  }
"""

VALID_SDP_OBJECT_PI20 = SDPConfiguration(
    interface="https://schema.skao.int/ska-sdp-assignres/0.4",
    execution_block=ExecutionBlockConfiguration(
        eb_id="eb-test-20220916-00000",
        max_length=3600.0,
        context={},
        beams=[BeamConfiguration(beam_id="vis0", function="visibilities")],
        scan_types=[
            EBScanType(
                scan_type_id=".default",
                beams={
                    "vis0": EBScanTypeBeam(
                        channels_id="vis_channels",
                        polarisations_id="all",
                    )
                },
            ),
            EBScanType(
                scan_type_id="target:a",
                derive_from=".default",
                beams={"vis0": EBScanTypeBeam(field_id="field_a")},
            ),
            EBScanType(
                scan_type_id="calibration:b",
                derive_from=".default",
                beams={"vis0": EBScanTypeBeam(field_id="field_b")},
            ),
        ],
        channels=[
            ChannelConfiguration(
                channels_id="vis_channels",
                spectral_windows=[
                    Channel(
                        spectral_window_id="fsp_1_channels",
                        count=4,
                        start=0,
                        stride=2,
                        freq_min=350000000.0,
                        freq_max=368000000.0,
                        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
                    )
                ],
            )
        ],
        polarisations=[
            PolarisationConfiguration(
                polarisations_id="all",
                corr_type=["XX", "XY", "YX", "YY"],
            )
        ],
        fields=[
            FieldConfiguration(
                field_id="field_a",
                phase_dir={
                    "ra": [123],
                    "dec": [-60],
                    "reference_time": "...",
                    "reference_frame": "ICRF3",
                },
                pointing_fqdn="...",
            ),
            FieldConfiguration(
                field_id="field_b",
                phase_dir={
                    "ra": [123.0],
                    "dec": [-60.0],
                    "reference_time": "...",
                    "reference_frame": "ICRF3",
                },
                pointing_fqdn="...",
            ),
        ],
    ),
    processing_blocks=[
        ProcessingBlockConfiguration(
            pb_id="pb-test-20220916-00000",
            sbi_ids=["sbi-test-20220916-00000"],
            script=ScriptConfiguration(
                kind="realtime",
                name="test-receive-addresses",
                version="0.5.0",
            ),
            parameters={},
        )
    ],
    resources={
        "receptors": ["SKA001", "SKA002", "SKA003", "SKA004"],
    },
)

INVALID_SDP_OBJECT_PI20 = SDPConfiguration(
    interface="https://schema.skao.int/ska-sdp-assignres/0.4",
    execution_block=ExecutionBlockConfiguration(
        eb_id="eb-test-20220916-00000",
        max_length=3600.0,
        context={},
        beams=[
            BeamConfiguration(beam_id="vis0", function="pulsar search"),
            BeamConfiguration(beam_id="vis0", function="vlbi"),
        ],
        scan_types=[
            EBScanType(
                scan_type_id=".default",
                beams={
                    "vis0": EBScanTypeBeam(
                        channels_id="vis_channels",
                        polarisations_id="all",
                    )
                },
            ),
            EBScanType(
                scan_type_id="target:a",
                derive_from=".default",
                beams={"vis0": EBScanTypeBeam(field_id="field_a")},
            ),
            EBScanType(
                scan_type_id="calibration:b",
                derive_from=".default",
                beams={"vis0": EBScanTypeBeam(field_id="field_b")},
            ),
        ],
        channels=[
            ChannelConfiguration(
                channels_id="vis_channels",
                spectral_windows=[
                    Channel(
                        spectral_window_id="fsp_1_channels",
                        count=4,
                        start=0,
                        stride=2,
                        freq_min=350000000.0,
                        freq_max=368000000.0,
                        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
                    ),
                    Channel(
                        spectral_window_id="fsp_2_channels",
                        count=4,
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
                corr_type=["XX", "XY", "YX", "YY"],
            )
        ],
        fields=[
            FieldConfiguration(
                field_id="field_a",
                phase_dir={
                    "ra": [123],
                    "dec": [-60],
                    "reference_time": "...",
                    "reference_frame": "ICRF3",
                },
                pointing_fqdn="...",
            ),
            FieldConfiguration(
                field_id="field_b",
                phase_dir={
                    "ra": [123.0],
                    "dec": [-60.0],
                    "reference_time": "...",
                    "reference_frame": "ICRF3",
                },
                pointing_fqdn="...",
            ),
        ],
    ),
    processing_blocks=[
        ProcessingBlockConfiguration(
            pb_id="pb-test-20220916-00000",
            sbi_ids=["sbi-test-20220916-00000"],
            script=ScriptConfiguration(
                kind="realtime",
                name="test-receive-addresses",
                version="0.5.0",
            ),
            parameters={},
        )
    ],
    resources={
        "receptors": ["SKA001", "SKA002", "SKA003", "SKA004"],
    },
)

INVALID_SDP_JSON_PI20 = """{
    "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
    "resources": {
      "receptors": [
        "SKA001",
        "SKA002",
        "SKA003",
        "SKA004"
      ]
    },
    "execution_block": {
      "eb_id": "eb-test-20220916-00000",
      "context": {},
      "max_length": 3600.0,
      "beams": [
        {
          "beam_id": "vis0",
          "function": "pulsar search"
        },
         {
          "beam_id": "vis0",
          "function": "vlbi"
        }
      ],
      "scan_types": [
        {
          "scan_type_id": ".default",
          "beams": {
            "vis0": {
              "channels_id": "vis_channels",
              "polarisations_id": "all"
            }
          }
        },
        {
          "scan_type_id": "target:a",
          "derive_from": ".default",
          "beams": {
            "vis0": {
              "field_id": "field_a"
            }
          }
        },
        {
          "scan_type_id": "calibration:b",
          "derive_from": ".default",
          "beams": {
            "vis0": {
              "field_id": "field_b"
            }
          }
        }
      ],
      "channels": [
        {
          "channels_id": "vis_channels",
          "spectral_windows": [
            {
              "spectral_window_id": "fsp_1_channels",
              "count": 4,
              "start": 0,
              "stride": 2,
              "freq_min": 350000000.0,
              "freq_max": 368000000.0,
              "link_map": [
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
              "spectral_window_id": "fsp_2_channels",
              "count": 4,
              "start": 0,
              "stride": 2,
              "freq_min": 350000000.0,
              "freq_max": 368000000.0,
              "link_map": [
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
      "polarisations": [
        {
          "polarisations_id": "all",
          "corr_type": [
            "XX",
            "XY",
            "YX",
            "YY"
          ]
        }
      ],
      "fields": [
        {
          "field_id": "field_a",
          "phase_dir": {
            "ra": [
              123.0
            ],
            "dec": [
              -60.0
            ],
            "reference_time": "...",
            "reference_frame": "ICRF3"
          },
          "pointing_fqdn": "..."
        },
        {
          "field_id": "field_b",
          "phase_dir": {
            "ra": [
              123.0
            ],
            "dec": [
              -60.0
            ],
            "reference_time": "...",
            "reference_frame": "ICRF3"
          },
          "pointing_fqdn": "..."
        }
      ]
    },
    "processing_blocks": [
      {
        "pb_id": "pb-test-20220916-00000",
        "script": {
          "kind": "realtime",
          "name": "test-receive-addresses",
          "version": "0.5.0"
        },
        "sbi_ids": [
          "sbi-test-20220916-00000"
        ],
        "parameters": {
        }
      }
    ]
  }

"""

INVALID_MID_ASSIGNRESOURCESREQUEST_JSON = (
    """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
  "transaction_id":"txn-....-00001",
  "subarray_id": 1,
  "dish": {"receptor_ids": ["0001","0002","0003","0004","0005"]},
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

INVALID_MID_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
    transaction_id="txn-....-00001",
    subarray_id=1,
    dish_allocation=DishAllocation(
        receptor_ids=["0001", "0002", "0003", "0004", "0005"]
    ),
    sdp_config=VALID_SDP_OBJECT_PI16,
)

INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON = (
    """
{
  "interface": "https://schema.skao.int/ska-low-tmc-assignresources/3.1",
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
    + INVALID_SDP_JSON_PI20
    + """
}
"""
)


INVALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-assignresources/3.1",
    transaction_id="txn-....-00001",
    subarray_id="1",
    sdp_config=VALID_SDP_OBJECT_PI20,
)


VALID_LOW_ASSIGNRESOURCESREQUEST_JSON = (
    """
{
  "interface": "https://schema.skao.int/ska-low-tmc-assignresources/3.1",
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
    + VALID_SDP_JSON_PI20
    + """
}
"""
)

VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-assignresources/3.1",
    transaction_id="txn-....-00001",
    subarray_id=1,
    mccs=MCCSAllocate(subarray_beam_ids=[1], station_ids=[(1, 2)], channel_blocks=[3]),
    sdp_config=VALID_SDP_OBJECT_PI20,
)

INVALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-assignresources/3.1",
    transaction_id="txn-....-00001",
    subarray_id="1",
    mccs=MCCSAllocate(subarray_beam_ids=[1], station_ids=[(1, 2)], channel_blocks=[3]),
    sdp_config=INVALID_SDP_OBJECT_PI20,
)


SCAN_VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-scan/1.0",
  "scan_id":1,
  "start_time": 0.0
}
"""

SCAN_VALID_OBJECT = ScanRequest(
    interface="https://schema.skatelescope.org/ska-low-mccs-scan/1.0",
    scan_id=1,
    start_time=0.0,
)


def low_invalidator_fn(o: AssignResourcesRequest):
    # function to make a valid LOW AssignedResourcesRequest invalid
    o.mccs.subarray_beam_ids = [1, 2, 3]


def low_tmc_invalidator_fn(o: AssignResourcesRequest):
    # function to make a validLOW AssignedResourcesRequest invalid
    o.sdp_config.execution_block.beams[0].function = "vis"


def mid_invalidator_fn(o: AssignResourcesRequest):
    # function to make a valid MID AssignResourcesRequest invalid
    o.sdp_config.max_length = 10


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json,is_validate",
    [
        (
            AssignResourcesRequestSchema,
            VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT,
            None,
            VALID_MID_ASSIGNRESOURCESREQUEST_JSON,
            None,
            False,
        ),
        (
            AssignResourcesResponseSchema,
            VALID_MID_ASSIGNRESOURCESRESPONSE_OBJECT,
            None,
            VALID_MID_ASSIGNRESOURCESRESPONSE_JSON,
            None,
            False,
        ),
        (
            SDPConfigurationSchema,
            VALID_SDP_OBJECT,
            None,
            VALID_SDP_JSON,
            None,
            True,
        ),
        (
            SDPConfigurationSchema,
            VALID_SDP_OBJECT_PI16,
            None,
            VALID_SDP_JSON_PI16,
            None,
            True,
        ),
        (
            SDPConfigurationSchema,
            VALID_SDP_OBJECT_PI20,
            None,
            VALID_SDP_JSON_PI20,
            None,
            True,
        ),
        (
            AssignResourcesRequestSchema,
            VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
            low_tmc_invalidator_fn,
            VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
            None,
            True,
        ),
        (
            AssignResourcesRequestSchema,
            VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT_PI16,
            None,
            VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16,
            None,
            True,
        ),
        (
            AssignResourcesRequestSchema,
            VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT_PI16,
            mid_invalidator_fn,
            VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16,
            None,
            True,
        ),
        (
            AssignResourcesRequestSchema,
            VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT_PI16,
            None,
            VALID_MID_ASSIGNRESOURCESREQUEST_JSON_PI16,
            None,
            False,
        ),
        (
            ScanRequestSchema,
            SCAN_VALID_OBJECT,
            None,
            SCAN_VALID_JSON,
            None,
            True,
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
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls,
        instance,
        modifier_fn,
        valid_json,
        invalid_json,
        is_validate,
    )


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json,is_validate",
    [
        (
            AssignResourcesRequestSchema,
            INVALID_MID_ASSIGNRESOURCESREQUEST_OBJECT,
            mid_invalidator_fn,
            INVALID_MID_ASSIGNRESOURCESREQUEST_JSON,
            None,
            True,
        ),
    ],
)
def test_assignresources_serialisation_and_validation_invalid_json(
    schema_cls,
    instance,
    modifier_fn,
    valid_json,
    invalid_json,
    is_validate,
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly
    for invalid json and raise SchematicValidationError.
    """
    try:
        utils.test_schema_serialisation_and_validation(
            schema_cls,
            instance,
            modifier_fn,
            valid_json,
            invalid_json,
            is_validate,
        )

    except SchematicValidationError as error:
        assert error.message == (
            "receptor_ids are too many!Current Limit is 4,"
            "beams are too many! Current limit is 1,Invalid function for beams! "
            "Currently allowed visibilities,spectral windows are too many! Current limit = 1,"
            "Invalid input for channel_count! Currently allowed 14880,Invalid input for freq_min,"
            "Invalid input for freq_max,length of receptor_ids should be same as length of receptors"
        )


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json,is_validate",
    [
        (
            AssignResourcesRequestSchema,
            INVALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
            low_tmc_invalidator_fn,
            INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
            None,
            True,
        ),
    ],
)
def test_tmc_low_assignresources_serialisation_and_validation_invalid_json(
    schema_cls,
    instance,
    modifier_fn,
    valid_json,
    invalid_json,
    is_validate,
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly
    for invalid json and raise SchematicValidationError for TMC LOW.
    """
    try:
        utils.test_schema_serialisation_and_validation(
            schema_cls,
            instance,
            modifier_fn,
            valid_json,
            invalid_json,
            is_validate,
        )

    except SchematicValidationError as error:
        assert error.message == (
            "beams are too many! Current limit is 1,"
            "Invalid function for beams! Currently allowed visibilities,"
            "spectral windows are too many! Current limit = 1"
        )

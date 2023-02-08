"""
Unit tests for ska_tmc_cdm.schemas module.
"""

import copy
import json

import pytest

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
    ScriptConfiguration,
    SDPConfiguration,
)
from ska_tmc_cdm.schemas.central_node.assign_resources import (
    AssignResourcesRequestSchema,
    AssignResourcesResponseSchema,
)
from ska_tmc_cdm.schemas.central_node.sdp import SDPConfigurationSchema
from ska_tmc_cdm.utils import assert_json_is_equal

from .. import utils

VALID_SDP_JSON = """
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


VALID_SDP_OBJECT = SDPConfiguration(
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


VALID_MID_ASSIGNRESOURCESREQUEST_JSON = (
    """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
  "transaction_id":"txn-....-00001",
  "subarray_id": 1,
  "dish": {"receptor_ids": ["0001"]},
  "sdp": """
    + VALID_SDP_JSON
    + """
}
"""
)

VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
    transaction_id="txn-....-00001",
    subarray_id=1,
    dish_allocation=DishAllocation(receptor_ids=["0001"]),
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


VALID_ASSIGN_RESOURCE_JSON_PI16 = """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
  "transaction_id": "txn-....-00001",
  "subarray_id": 1,
  "dish": {
    "receptor_ids": [
      "0001"
    ]
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
    "execution_block": {
      "eb_id": "eb-mvp01-20200325-00001",
      "max_length": 100,
      "context": {},
      "beams": [
        {
          "beam_id": "vis0",
          "function": "visibilities"
        },
        {
          "beam_id": "pss1",
          "search_beam_id": 1,
          "function": "pulsar search"
        },
        {
          "beam_id": "pss2",
          "search_beam_id": 2,
          "function": "pulsar search"
        },
        {
          "beam_id": "pst1",
          "timing_beam_id": 1,
          "function": "pulsar timing"
        },
        {
          "beam_id": "pst2",
          "timing_beam_id": 2,
          "function": "pulsar timing"
        },
        {
          "beam_id": "vlbi1",
          "vlbi_beam_id": 1,
          "function": "vlbi"
        }
      ],
      "channels": [
        {
          "channels_id": "vis_channels",
          "spectral_windows": [
            {
              "count": 744,
              "start": 0,
              "stride": 2,
              "freq_min": 350000000,
              "freq_max": 368000000,
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
              "count": 744,
              "start": 2000,
              "stride": 1,
              "freq_min": 360000000,
              "freq_max": 368000000,
              "link_map": [
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
              "spectral_window_id": "zoom_window_1",
              "count": 744,
              "start": 4000,
              "stride": 1,
              "freq_min": 360000000,
              "freq_max": 361000000,
              "link_map": [
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
        },
        {
          "channels_id": "pulsar_channels",
          "spectral_windows": [
            {
              "spectral_window_id": "pulsar_fsp_channels",
              "count": 744,
              "start": 0,
              "freq_min": 350000000,
              "freq_max": 368000000
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
            "YY",
            "YX"
          ]
        }
      ],
      "fields": [
        {
          "field_id": "field_a",
          "phase_dir": {
            "ra": [
              123,
              0.1
            ],
            "dec": [
              123,
              0.1
            ],
            "reference_time": "...",
            "reference_frame": "ICRF3"
          },
          "pointing_fqdn": "low-tmc/telstate/0/pointing"
        }
      ]
    },
    "processing_blocks": [
      {
        "pb_id": "pb-mvp01-20200325-00001",
        "sbi_ids": [
          "sbi-mvp01-20200325-00001"
        ],
        "script": {},
        "parameters": {},
        "dependencies": []
      },
      {
        "pb_id": "pb-mvp01-20200325-00002",
        "sbi_ids": [
          "sbi-mvp01-20200325-00002"
        ],
        "script": {},
        "parameters": {},
        "dependencies": []
      },
      {
        "pb_id": "pb-mvp01-20200325-00003",
        "sbi_ids": [
          "sbi-mvp01-20200325-00001",
          "sbi-mvp01-20200325-00002"
        ],
        "script": {},
        "parameters": {},
        "dependencies": []
      }
    ],
    "resources": {
      "csp_links": [
        1,
        2,
        3,
        4
      ],
      "receptors": [
        "FS4",
        "FS8"
      ],
      "receive_nodes": 10
    }
  }
}"""

VALID_ASSIGN_RESOURCE_WITH_SDP_ALL_PARAMETERS_JSON_PI16 = """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
  "transaction_id": "txn-....-00001",
  "subarray_id": 1,
  "dish": {
    "receptor_ids": [
      "0001"
    ]
  },
  "sdp": {
   "interface":"https://schema.skao.int/ska-sdp-assignres/0.4",

   "resources": {
      "csp_links": [ 1, 2, 3, 4 ],
      "receptors": ["C10", "C136", "C1", "C217", "C13", "C42"],
      "receive_nodes": 1
   },

   "execution_block": {
      "eb_id":"eb-test-20210630-00000",
      "context": {},
      "max_length":21600.0,

      "channels": [ {
         "channels_id": "vis_channels",
         "spectral_windows": [ {
             "spectral_window_id": "fsp_1_channels",
             "count": 13824,
             "start": 0,
             "stride": 2,
             "freq_min": 0.35e9,
             "freq_max": 0.368e9,
             "link_map": [ [0, 0], [200, 1], [744, 2], [944, 3] ]
         } ]
      } ],

      "polarisations": [ {
         "polarisations_id": "all",
         "corr_type": [ "XX", "XY", "YY", "YX" ]
      } ],

      "fields": [ {
         "field_id": "field_a",
         "phase_dir" : {
           "ra": [ 2.711325 ],
           "dec": [ -0.01328889 ],
           "reference_time": "...",
           "reference_frame": "ICRF3"
         },
         "pointing_fqdn": "low-tmc/telstate/0/pointing"
      }, {
         "field_id": "field_b",
         "phase_dir" : {
           "ra": [ 12.48519 ],
           "dec": [ 2.052388 ],
           "reference_time": "...",
           "reference_frame": "ICRF3"
         },
         "pointing_fqdn": "low-tmc/telstate/0/pointing"
      } ],

      "beams": [ {
         "beam_id": "vis0",
         "function": "visibilities"
      } ],

      "scan_types":[
         {
            "scan_type_id": ".default",
            "beams": {
               "vis0": {
                  "polarisations_id": "all",
                  "channels_id": "vis_channels"
               }
            }
         },
         {
            "scan_type_id": "science",
            "derive_from": ".default",
            "beams": {
              "vis0": { "field_id": "field_a" }
            }
         },
         {
            "scan_type_id": "calibration",
            "derive_from": ".default",
            "beams": {
              "vis0": { "field_id": "field_b" }
            }
         }
      ]
   },
   "processing_blocks":[
      {
         "pb_id":"pb-test-20211111-00000",
         "script":{
            "kind":"realtime",
            "name":"vis-receive",
            "version":"0.6.0"
         },
         "parameters": {
            "plasmaEnabled": true,
            "reception": {
               "layout": "http://127.0.0.1:80/model/default/ska1_low/layout",
               "num_channels": 13824,
               "channels_per_stream": 6912,
               "continuous_mode": true,
               "transport_protocol": "tcp"
            },
            "pvc": {
               "name": "receive-data"
            },
            "plasma_parameters": {
               "initContainers":[
                  {
                     "name":"existing-output-remover",
                     "image":"artefact.skao.int/ska-sdp-realtime-receive-modules:3.3.0",
                     "command":["rm", "-rf", "/mnt/data/output*.ms"],
                     "volumeMounts":[
                        {
                           "mountPath":"/mnt/data",
                           "name":"receive-data"
                        }
                     ]
                  }
               ],
               "extraContainers":[
                  {
                     "name":"plasma-processor",
                     "image":"artefact.skao.int/ska-sdp-realtime-receive-modules:3.3.0",
                     "command":[
                        "plasma-mswriter",
                        "-s",
                        "/plasma/socket",
                        "--max_payloads",
                        "12",
                        "--use_plasmastman",
                        "False",
                        "/mnt/data/output.ms"
                     ],
                     "volumeMounts":[
                        {
                           "name":"plasma-storage-volume",
                           "mountPath":"/plasma"
                        },
                        {
                           "mountPath":"/mnt/data",
                           "name":"receive-data"
                        }
                     ]
                  },
                  {
                     "name": "tmlite-server",
                     "image": "artefact.skao.int/ska-sdp-tmlite-server:0.3.0"
                  }
               ]
            }
         }
      }
   ]
}
}"""

VALID_ASSIGN_RESOURCE_WITH_SDP_MINIMAL_PARAMETERS_JSON_PI16 = """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
  "transaction_id": "txn-....-00001",
  "subarray_id": 1,
  "dish": {
    "receptor_ids": [
      "0001"
    ]
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
    "resources": {    
        "receptors": ["SKA001", "SKA036", "SKA063", "SKA100"]
    },
    "execution_block": {
        "eb_id": "eb-mvp01-20220929-00000",
        "max_length": 3600.0,
        "context": {},
        "beams": [{ "beam_id": "vis0", "function": "visibilities" }],
        "scan_types": [{
            "scan_type_id": ".default",
            "beams": { "vis0": { "channels_id": "vis_channels", "polarisations_id": "all" } }
        }, {
            "scan_type_id": "science:target",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "science-target" } }
        }, {
            "scan_type_id": "flux:pks1934-638",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "pks1934-638" } }
        }, {
            "scan_type_id": "delay:TBD",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "delay-field-TBD" } }
        }, {
            "scan_type_id": "bandpass:pks1921-203",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "pks1921-203" } }
        }, {
            "scan_type_id": "gains:TBD",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "gains-field-TBD" } }
        }, {
            "scan_type_id": "polarisation:TBD",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "polarisation-field-TBD" } }
        }],
        "channels": [{
            "channels_id": "vis_channels",
            "spectral_windows": [{
                "spectral_window_id": "fsp_1_channels",
                "count": 14480, "start": 0, "stride": 1,
                "freq_min": 950000000.0, "freq_max": 1170000000.0,
                "link_map": [ [0, 0] ]
            }]
        }],
        "polarisations": [{
            "polarisations_id": "all",
            "corr_type": ["XX", "XY", "YY", "YX"]
        }],
        "fields": [{
            "field_id": "science-target",
            "phase_dir": {
                "ra": [-1], "dec": [-1],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        },{
            "field_id": "pks1934-638",
            "phase_dir": {
                "ra": [294.85426888], "dec": [-63.71267788],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        },{
            "field_id": "delay-field-TBD",
            "phase_dir": {
                "ra": [-1], "dec": [-1],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        },{
            "field_id": "pks1921-203",
            "phase_dir": {
                "ra": [291.21273125], "dec": [-29.23892167],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        }]
    },
  "processing_blocks": [
    {
      "pb_id": "pb-test-20220916-00000",
      "script": {"kind": "realtime", "name": "test-receive-addresses", "version": "0.5.0"},
      "sbi_ids": ["sbi-test-20220916-00000"],
      "parameters": {}
    }
]
}
}"""

VALID_LOW_ASSIGN_RESOURCE_JSON_PI17 = """
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
    "sdp": {
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
            "max_length": 3600,
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
                            "freq_min": 350000000,
                            "freq_max": 368000000,
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
                            123
                        ],
                        "dec": [
                            -60
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
                            123
                        ],
                        "dec": [
                            -60
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
    },
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


def low_invalidator_fn(o: AssignResourcesRequest):
    # function to make a valid LOW AssignedResourcesRequest invalid
    o.mccs.subarray_beam_ids = [1, 2, 3]


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            AssignResourcesRequestSchema,
            VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
            low_invalidator_fn,
            VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
            INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
        ),
        (
            AssignResourcesRequestSchema,
            VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT,
            None,  # No validation for MID
            VALID_MID_ASSIGNRESOURCESREQUEST_JSON,
            None,
        ),  # No validation for MID
        (
            AssignResourcesResponseSchema,
            VALID_MID_ASSIGNRESOURCESRESPONSE_OBJECT,
            None,  # No validation for MID
            VALID_MID_ASSIGNRESOURCESRESPONSE_JSON,
            None,
        ),  # No validation for MID
        (
            SDPConfigurationSchema,
            VALID_SDP_OBJECT,
            None,  # No validation on SDP subschema
            VALID_SDP_JSON,
            None,
        ),  # No validation on SDP subschema
    ],
)
def test_assignresources_serialisation_and_validation(
    schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )


def test_assignresources_serialisation_and_validation_without_optional_params():
    valid_json_no_optional_params = json.loads(
        copy.deepcopy(VALID_MID_ASSIGNRESOURCESREQUEST_JSON)
    )
    del valid_json_no_optional_params["sdp"]["interface"]
    del valid_json_no_optional_params["interface"]

    request = copy.deepcopy(VALID_MID_ASSIGNRESOURCESREQUEST_OBJECT)
    request.sdp_config.interface = None
    request.interface = None

    utils.test_schema_serialisation_and_validation(
        AssignResourcesRequestSchema,
        request,
        None,
        json.dumps(valid_json_no_optional_params),
        None,
    )


def test_validate_serialization_and_deserialization_assign_resource_using_schema_class():
    """
    Verifies that the Assign Resource schema marshal and Unmarshal works correctly
    """
    assign_resource_config = AssignResourcesRequestSchema().loads(
        VALID_ASSIGN_RESOURCE_JSON_PI16
    )
    serialized_assign_resource_config = AssignResourcesRequestSchema().dumps(
        assign_resource_config
    )

    assert_json_is_equal(
        VALID_ASSIGN_RESOURCE_JSON_PI16, serialized_assign_resource_config
    )


def test_validate_serialization_and_deserialization_assign_resource_with_sdp_all_parameters_using_schema_class():
    """
    Verifies that the Assign Resource schema marshal and Unmarshal works correctly
    """
    assign_resource_config = AssignResourcesRequestSchema().loads(
        VALID_ASSIGN_RESOURCE_WITH_SDP_ALL_PARAMETERS_JSON_PI16
    )
    serialized_assign_resource_config = AssignResourcesRequestSchema().dumps(
        assign_resource_config
    )

    assert_json_is_equal(
        VALID_ASSIGN_RESOURCE_WITH_SDP_ALL_PARAMETERS_JSON_PI16,
        serialized_assign_resource_config,
    )


def test_validate_serialization_and_deserialization_assign_resource_with_sdp_minimal_parameters_using_schema_class():
    """
    Verifies that the Assign Resource schema marshal and Unmarshal works correctly
    """
    assign_resource_config = AssignResourcesRequestSchema().loads(
        VALID_ASSIGN_RESOURCE_WITH_SDP_MINIMAL_PARAMETERS_JSON_PI16
    )
    serialized_assign_resource_config = AssignResourcesRequestSchema().dumps(
        assign_resource_config
    )

    assert_json_is_equal(
        VALID_ASSIGN_RESOURCE_WITH_SDP_MINIMAL_PARAMETERS_JSON_PI16,
        serialized_assign_resource_config,
    )


def test_validate_serialization_and_deserialization_low_assign_resource():
    """
    Verifies that the PI 17 Low Assign Resource schema
    with both sdp and csp block
    marshal and unmarshal works correctly
    """

    assign_resource_config = AssignResourcesRequestSchema().loads(
        VALID_LOW_ASSIGN_RESOURCE_JSON_PI17
    )

    assert_json_is_equal(
        VALID_LOW_ASSIGN_RESOURCE_JSON_PI17,
        AssignResourcesRequestSchema().dumps(assign_resource_config),
    )

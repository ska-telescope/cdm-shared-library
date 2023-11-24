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
    ScriptConfiguration,
    SDPConfiguration,
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


VALID_SDP_JSON = """
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

VALID_SDP_OBJECT = SDPConfiguration(
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


INVALID_SDP_OBJECT = SDPConfiguration(
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
                        freq_min=35000000.0,
                        freq_max=49880000000000.0,
                        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
                    ),
                    Channel(
                        spectral_window_id="fsp_2_channels",
                        count=4,
                        start=0,
                        stride=2,
                        freq_min=360000000.0,
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

INVALID_SDP_JSON = """{
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
              "freq_min": 35000000.0,
              "freq_max": 49880000000000.0,
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
              "freq_min": 360000000.0,
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
    + INVALID_SDP_JSON
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
    + INVALID_SDP_JSON
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
    sdp_config=INVALID_SDP_OBJECT,
)

INVALID_LOW_ASSIGNRESOURCESREQUEST_JSON = (
    """
{
  "interface": "https://schema.skao.int/ska-low-tmc-assignresources/3.2",
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
    + INVALID_SDP_JSON
    + """
}
"""
)


VALID_LOW_ASSIGNRESOURCESREQUEST_JSON = (
    """
{
  "interface": "https://schema.skao.int/ska-low-tmc-assignresources/3.2",
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
    + VALID_SDP_JSON
    + """
}
"""
)

VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-assignresources/3.2",
    transaction_id="txn-....-00001",
    subarray_id=1,
    mccs=MCCSAllocate(subarray_beam_ids=[1], station_ids=[(1, 2)], channel_blocks=[3]),
    sdp_config=VALID_SDP_OBJECT,
)

INVALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-assignresources/3.2",
    transaction_id="txn-....-00001",
    subarray_id="1",
    mccs=MCCSAllocate(subarray_beam_ids=[1], station_ids=[(1, 2)], channel_blocks=[3]),
    sdp_config=INVALID_SDP_OBJECT,
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
            AssignResourcesRequestSchema,
            VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
            low_tmc_invalidator_fn,
            VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
            None,
            True,
        ),
        (
            AssignResourcesRequestSchema,
            VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
            None,
            VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
            None,
            True,
        ),
        (
            AssignResourcesRequestSchema,
            VALID_LOW_ASSIGNRESOURCESREQUEST_OBJECT,
            None,
            VALID_LOW_ASSIGNRESOURCESREQUEST_JSON,
            None,
            False,
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
            "Invalid input for freq_max,length of receptor_ids should be same as length of receptors,"
            "receptor_ids did not match receptors"
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

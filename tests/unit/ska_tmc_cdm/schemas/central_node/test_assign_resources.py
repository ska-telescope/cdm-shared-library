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
from ska_tmc_cdm.messages.central_node.csp import (
    CommonConfiguration,
    CSPConfiguration,
    LowCbfConfiguration,
    ResourcesConfiguration,
)
from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate
from ska_tmc_cdm.messages.central_node.sdp import (
    Channel,
    PbDependency,
    ProcessingBlockConfiguration,
    ScanType,
    SDPConfiguration,
    SDPWorkflow,
)
from ska_tmc_cdm.schemas.central_node.assign_resources import (
    AssignResourcesRequestSchema,
    AssignResourcesResponseSchema,
)
from ska_tmc_cdm.schemas.central_node.sdp import SDPConfigurationSchema
from ska_tmc_cdm.utils import assert_json_is_equal

from .. import utils

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

VALID_LOW_ASSIGN_RESOURCE_WITH_CSP_JSON_PI17 = """
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

VALID_LOW_ASSIGN_RESOURCE_WITH_CSP_OBJECT_PI17 = AssignResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-assignresources/3.0",
    transaction_id="txn-....-00001",
    subarray_id=1,
    mccs=MCCSAllocate(subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]),
    csp_config=CSPConfiguration(
        interface="https://schema.skao.int/ska-low-csp-assignresources/2.0",
        common=CommonConfiguration(subarray_id=1),
        lowcbf=LowCbfConfiguration(
            resources=[
                ResourcesConfiguration(
                    device="fsp_01", shared=True, fw_image="pst", fw_mode="unused"
                ),
                ResourcesConfiguration(
                    device="p4_01", shared=True, fw_image="p4.bin", fw_mode="p4"
                ),
            ]
        ),
    ),
)


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


def test_validate_serialization_and_deserialization_low_assign_resource_with_csp_parameters_using_schema_class():
    """
    Verifies that the Assign Resource schema marshal and Unmarshal works correctly
    """

    serialized_assign_resource_config = AssignResourcesRequestSchema().dumps(
        AssignResourcesRequestSchema().loads(
            VALID_LOW_ASSIGN_RESOURCE_WITH_CSP_JSON_PI17
        )
    )

    assert_json_is_equal(
        AssignResourcesRequestSchema().dumps(
            VALID_LOW_ASSIGN_RESOURCE_WITH_CSP_OBJECT_PI17
        ),
        serialized_assign_resource_config,
    )

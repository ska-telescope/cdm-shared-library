from ska_tmc_cdm import CODEC
from ska_tmc_cdm.messages.central_node.csp import CSPConfiguration
from ska_tmc_cdm.utils import assert_json_is_equal

VALID_CSP_LOW_JSON = """ {
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
  }"""


def test_validate_serialization_and_deserialization_CSPConfiguration_json():
    """
    Verifies that the CSPConfiguration de/serialises correctly.
    """

    csp_configuration_object = CODEC.loads(
        CSPConfiguration, VALID_CSP_LOW_JSON
    )
    serialized_csp_config = CODEC.dumps(csp_configuration_object)
    assert_json_is_equal(VALID_CSP_LOW_JSON, serialized_csp_config)

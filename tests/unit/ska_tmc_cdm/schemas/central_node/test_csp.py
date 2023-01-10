from ska_tmc_cdm.schemas.central_node.csp import CSPConfigurationSchema
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


def test_validate_serialization_and_deserialization_CSPConfiguration_json_using_schema_class():
    """
    Verifies that the CSPConfiguration schema marshal and Unmarshal works correctly
    """

    csp_configuration_object = CSPConfigurationSchema().loads(VALID_CSP_LOW_JSON)
    serialized_csp_config = CSPConfigurationSchema().dumps(csp_configuration_object)

    assert_json_is_equal(VALID_CSP_LOW_JSON, serialized_csp_config)

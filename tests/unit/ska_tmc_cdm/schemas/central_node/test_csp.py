from ska_tmc_cdm.schemas.central_node.csp import CSPLowConfigurationSchema
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


def test_validate_serialization_and_deserialization_csplowconfiguration_json_using_schema_class():
    """
    Verifies that the CSPLowConfiguration schema marshal and Unmarshal works correctly
    """

    csp_configuration_object = CSPLowConfigurationSchema().loads(VALID_CSP_LOW_JSON)
    serialized_csp_config = CSPLowConfigurationSchema().dumps(csp_configuration_object)

    assert_json_is_equal(VALID_CSP_LOW_JSON, serialized_csp_config)

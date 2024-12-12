from ska_tmc_cdm import CODEC
from ska_tmc_cdm.messages.central_node.csp import CSPConfiguration

from .....utils import assert_json_is_equal

VALID_CSP_LOW_JSON = """
{
  "pss": {
    "pss_beam_ids": [
      1,
      2,
      3
    ]
  },
  "pst": {
    "pst_beam_ids": [
      1
    ]
  }
}      
"""


def test_validate_serialization_and_deserialization_CSPConfiguration_json():
    """
    Verifies that the CSPConfiguration de/serialises correctly.
    """

    csp_configuration_object = CODEC.loads(
        CSPConfiguration, VALID_CSP_LOW_JSON
    )
    serialized_csp_config = CODEC.dumps(csp_configuration_object)
    assert_json_is_equal(VALID_CSP_LOW_JSON, serialized_csp_config)

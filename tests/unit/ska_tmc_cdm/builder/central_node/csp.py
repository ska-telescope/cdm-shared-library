import functools

from ska_tmc_cdm.messages.central_node.csp import (
    CSPConfiguration,
    PSSConfiguration,
    PSTConfiguration,
)

PSSConfigurationBuilder = functools.partial(
    PSSConfiguration, pss_beam_ids=(1, 2, 3)
)

PSTConfigurationBuilder = functools.partial(
    PSTConfiguration, pst_beam_ids=(1, 2, 3)
)

CSPConfigurationBuilder = functools.partial(
    CSPConfiguration,
    pss=PSSConfigurationBuilder(),
    pst=PSTConfigurationBuilder(),
)

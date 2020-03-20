================================
cdm-shared-library documentation
================================

.. COMMUNITY SECTION ==================================================

.. Hidden toctree to manage the sidebar navigation.

.. toctree::
  :maxdepth: 2
  :caption: Table of Contents
  :hidden:

  developer/developer
  developer/centralnode/centralnode
  developer/subarraynode/subarraynode
  client

- :doc:`developer/developer`
- :doc:`developer/centralnode/centralnode`
- :doc:`developer/subarraynode/subarraynode`
- :doc:`client`

Project description
===================

cdm-shared-library provides a Python object model and serialisation library
that assists in creating correctly formatted JSON arguments for resource
allocation commands and telescope configuration commands. It can be considered
an ICD support library, intended to be used by the Tango clients and Tango
servers on opposing sides of a telescope control interface.

Status
------

This library supports the PI#3 version of the CDM, as
`summarised on SKA Confluence <https://confluence.skatelescope.org/x/ARN0B>`_.

Additional material on the PI#3 schema can be found at the links below:

* `<https://confluence.skatelescope.org/display/SE/CSP_Mid+Scan+Configuration+for+Correlation>`_
* `<https://confluence.skatelescope.org/pages/viewpage.action?pageId=74716479>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


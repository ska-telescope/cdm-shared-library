.. _`Developer Documentation`:

=======================
Developer Documentation
=======================

Quickstart
==========

This project is structured to use Docker containers for development and
testing so that the build environment, test environment and test results are
all completely reproducible and are independent of host environment. It uses
``make`` to provide a consistent UI (see `Makefile targets`_).

Build a new Docker image and execute the test suite with:

::

  make oci-build


Execute the test suite and lint the project with:

::

  make python-test && make python-lint

Format the Python code:

::

  make python-format


Makefile targets
================
This project contains a `Makefile Gitlab Submodule  <https://gitlab.com/ska-telescope/sdi/ska-cicd-makefile>`_ which acts as a UI for building Docker
images, testing images, and for launching interactive developer environments.
The following make targets are defined:

+-----------------+------------------------------------------------+
| Makefile target | Description                                    |
+=================+================================================+
| oci-build       | Build a new application image                  |
+-----------------+------------------------------------------------+
| python-test     | Test the application image                     |
+-----------------+------------------------------------------------+
| python-lint     | Lint the application image                     |
+-----------------+------------------------------------------------+
| python-format   |  Format the Python code                        |
+-----------------+------------------------------------------------+
| help            | show a summary of the makefile targets above   |
+-----------------+------------------------------------------------+


Background
==========

SKA Tango devices have commands that accept structured arguments and/or return
structured responses. These structured data are often expressed as
JSON-formatted strings.

The Configuration Data Model (CDM) is a data model used to describe subarray
resource allocations and the subsequent configuration of those resources. It
is effectively the superset of the configurations used by receptors,
correlators, and data processing systems. The CDM is one such example of
structured data delivered to TMC Tango devices.

This project defines object representations of the structured data passed to
and from Tango devices, and serialisation schema used to convert the
structured data to and from JSON. This project defines:

#. a Python object model of the CDM;
#. a Python object model for the structured arguments sent to TMC Tango
   devices and the structured responses received in return;
#. serialisation schema to convert the Python object model instances to and
   from JSON.
#. validation of the JSON strings sent between devices are compliant with
   the agreed interfaces.

The primary users of this shared library are the OET, SubArrayNode, and
CentralNode. The OET uses this library to construct object representations of
telescope configurations and resource allocation instructions, to convert
those object representations to JSON-formatted payloads for TMC devices, and
finally to convert the JSON responses returned by TMC devices back into Python
objects.

It is intended that TMC devices also use this library to guarantee
correct data exchange with the OET. TMC can also use this library to marshall
and unmarshall its arguments to CSP and SDP Tango devices, which accept the
appropriate subset of the JSON.

Project layout
==============

The CDM project contains three top-level packages, ``ska_tmc_cdm.messages``,
``ska_tmc_cdm.schemas`` and ``ska_tmc_cdm.jsonschema`` as shown in the figure below. 
The ``ska_tmc_cdm.messages``
package contains Python object models for the JSON command arguments agreed
in the ICDs. The ``ska_tmc_cdm.schemas`` package contains code to transform the
classes defined in ``ska_tmc_cdm.messages`` to and from JSON. 
The ``ska_tmc_cdm.jsonschema`` package contains
code to verify that the JSON strings sent between devices are compliant with the agreed interfaces.

.. figure:: layout.png
   :align: center
   :alt: project layout

   Project layout and naming conventions.

The project layout and naming conventions are:

* Each Tango device has a corresponding Python sub-package in
  ``ska_tmc_cdm.messages`` and ``ska_tmc_cdm.schemas``.
* Code and schema for each Tango device command are located in Python modules
  inside their respective package.
* Structured input for the Tango command is modelled by a ``Request`` object.
* Structured output from the command is modelled by a ``Response`` object.
* Marshmallow schema are created to transform Python ``Request`` and
  ``Response`` instances to an from JSON, along with any other content they
  contain.

Messages
--------

The Python object model for the JSON defined in the ICD is located in the
``ska_tmc_cdm.messages`` package. In general, each CDM JSON entity is represented
as a Python class and each CDM attribute presented as a class property.

CDM attributes can be typed as plain Python data types (strings, floats, etc.)
or, where appropriate, represented by rich objects if this provides additional
value to the client. For example, while astronomical coordinates are
represented by floats and strings in the JSON schema, in the object model they
are defined as Astropy
`SkyCoord <https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html>`_
instances to ensure ensure correct coordinate handling and permit easier
manipulation downstream. Similarly, quantities with units could be defined as
instances of Astropy
`Quantity <https://docs.astropy.org/en/stable/units/quantity.html>`_ to
provide additional functionality.

For details on the device messages modelled by this library, see:

- :doc:`centralnode/centralnode`
- :doc:`subarraynode/subarraynode`
- :doc:`mccscontroller/mccscontroller`
- :doc:`mccssubarray/mccssubarray`


Marshmallow Schemas
-------------------

Classes to marshall the ``ska_tmc_cdm.messages`` objects to and from JSON are
defined in the ``ska_tmc_cdm.schemas`` package. The ska-tmc-cdm project
uses `Marshmallow <http://marshmallow.org>`_ for JSON serialisation. Classes
in the ``ska_tmc_cdm.schemas`` define Marshmallow schemas which are used by
Marshmallow during JSON conversion.

.. figure:: schema_cn.png
   :align: center
   :alt: CentralNode schema

   Schema mapping for objects used to communicate with TMC CentralNode device.

.. figure:: schema_san.png
   :align: center
   :alt: SubArrayNode schema

   Schema mapping for objects used to communicate with TMC SubArrayNode device.

.. figure:: schema_mccscontroller.png
   :align: center
   :alt: MCCSController schema

   Schema mapping for objects used to communicate with MCCSController device.

.. figure:: schema_mccssubarray.png
   :align: center
   :alt: MCCSSubArray schema

   Schema mapping for objects used to communicate with MCCSSubarray device.


JSON Schemas
------------

The CDM library uses the `SKA Telescope Model <https://developer.skatelescope.org/projects/telescope-model/en/latest/README.html>`_
to ensure the JSON accepted and JSON generated by the library are compliant
with the schema declared by the data.

The entry points for code handling JSON schema validation is located in
the ``ska_tmc_cdm.jsonschema`` module. This module contains methods for fetching
version-specific JSON schemas using interface URI and validating the structure
of JSON against these schemas. Json Schema validation functionality is enabled
by default with the parameter ``validate=True`` when converting a
JSON string to CDM using ``ska_tmc_cdm.schemas.CODEC.loads()`` and when converting
CDM to a JSON string using ``ska_tmc_cdm.schemas.CODEC.dumps()``.

.. figure:: json_schema.png
   :align: center
   :alt: JSON schema Validation


Extending the CDM
=================

Additional devices and applications cay use this library to communicate CDM
elements wherever useful. Developers are encouraged to extend the
ska-tmc-cdm project, adding object models and schemas for the
structured arguments for their Tango devices.

The steps to extend the CDM are:

#. Create a new package for the Tango device in ``ska_tmc_cdm.messages``.
#. For each device command, create a new module in the new package.
#. If the command accepts structured input, define a ``Request`` class in the
   module.
#. If the command returns a structured response, define a ``Response`` class in
   the module.
#. With the Python object model defined, create a corresponding package and
   module structure in ``ska_tmc_cdm.schemas``.
#. In the schema module, define Marshmallow schemas to convert the object
   model classes and any structure to JSON.
#. If this is a major entity, register the schema with the
   ``ska_tmc_cdm.schemas.CODEC`` object using the ``@CODEC.register_mapping``
   decorator.

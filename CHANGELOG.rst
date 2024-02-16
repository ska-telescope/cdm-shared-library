###########
Change Log
###########

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`_.

[8.3.0]
*******

* Updated version of telmodel which has first (early) version of Observatory Static Data (OSD).
  Added semantic validation support for SBD.

[8.2.0]
*******

* Updated version of telmodel which has semantic valdiation for SBD.
  Added new rule, next line support and modified frequency min max ranges in 
  existing semantic validation test-cases.
  Added default schema to AssignResourcesRequest, ReleaseResourcesRequest and 
  ConfigureRequest.

[8.1.0]
*******

* Added PI-20 low schema support.
  Added semantic validation support for PI-20 low schema.

[8.0.1]
*******

* Fixes an AttributeError when SKA_TELMODEL_SOURCES not set.

[8.0.0]
*******

Added
-----

* Support for TMC.partial_configuration and Target offset parameters.

Changed
-------

* All classes in ska_tmc_cdm.messages are now Python dataclasses with
  Pydantic valdiation. This will enforce runtime type-checking that may
  break callers passing invalid types.

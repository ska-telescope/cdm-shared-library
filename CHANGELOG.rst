###########
Change Log
###########

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`_.

[8.1.0]
*******

* Added PI-20 low schema support.
  Added symantic validation support for PI-20 low schema.

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

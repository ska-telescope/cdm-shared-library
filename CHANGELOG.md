Change Log
==========

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

9.1.1
*****

* BTN-2332 - Updated the make submodule, Updated RtD Theme and added Changelog to RtD

9.1.0
*****

* BTN-2265 - Added ability to apply, maintain or reset a previously calculated reference pointing calibration

9.0.0
*****

* Utilised ska_telmodel v1.15.1 with OSO-TMC low configure schema 3.2
* Created class for low cbf VIS station beams configurations
* SAH-1500 - Update low delay model calculation to accept Ra-Dec in configure command
* CT-1244 - Support other teams

* Updated existing unit tests and add new tests

8.3.0
*****

* Updated version of ska_telmodel which has first (early) version of Observatory Static Data (OSD)
*  Added semantic validation support for SBD

8.2.0
*****

* Updated version of ska_telmodel which has semantic validation for SBD
* Added new rule, next line support and modified frequency min max ranges in 
  existing semantic validation test-cases.
* Added default schema to AssignResourcesRequest, ReleaseResourcesRequest and 
  ConfigureRequest

8.1.0
*****

* Added PI-20 low schema support
* Added semantic validation support for PI-20 low schema

8.0.1
*****

* Fixes an AttributeError when SKA_TELMODEL_SOURCES not set

8.0.0
*****

* Support for TMC.partial_configuration and Target offset parameters
* All classes in ska_tmc_cdm.messages are now Python dataclasses with
  Pydantic validation. This will enforce runtime type-checking that may
  break callers passing invalid types

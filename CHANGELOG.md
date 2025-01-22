Change Log
==========

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased
* Bug fix: Updated default schema for Mid TMC Configure from `4.0` to `4.1`
* Bug fix: Updated default projection for trajectory offsets to `SIN`

## 12.6.3
* Bug fix: Updated `configure.subarray_node.core._TargetBase` to allow ra/dec to be 0.

## 12.6.2
* Bug fix: updated documentation

## 12.6.1
* Bug fix: updated `FixedTrajectory` object to have `attrs` kwarg and removed 't' list of timestamps
* Bug fix: TableTrajectory x and y attributes made lists of floats to match revised ADR-106
* Bug fix: aligned Projection defaults with revised ADR-106
* Bug fix: makes 'field' and 'receptors' optional in a receptor group, to align with revised ADR-106 and OSO/TMC
  agreement.
* Bug fix: removes MosaicTrajectory, reflecting removal of mosaic trajectory in ADR-106


## 12.6.0
* Updated to astropy v6.1, pydantic v2.10.3, deepdiff v7.0 and ska-ost-osd v 2.3.1

## 12.5.1
* Updated default schema for Mid TMC Configure from `2.3` to `4.0`
* Bug fix: Updated `(Special)Target.reference_frame` to be case-insensitive on read but convert to correct case on write

## 12.5.0
* Added VALIDATION_STRICTNESS environment variable to enable the functionality of semantic validation to turn on/off.
* Integrated latest OSD version into CDM.

## 12.4.0
* Added a new `messages.skydirection` module containing classes for ADR-63 sky directions, which are all unified under
  a `messages.skydirection.SkyDirection` union. The `SkyDirection` union should be used whenever an SKA-standard target
  coordinate is required.
* `ReceptorGroup.field` now uses an ADR-63 `SkyDirection`.
* **DEPRECATED** `pointing.target` now deprecated and will be removed in a future release. Developers should start
    populating `ReceptorGroup` and `ReceptorGroup.field` objects. `pointing.Target` should continue to be populated
    where the reference frame and observation type allows, i.e., a simple point-and-stare at an ICRS coordinate.
* PST beams now have an optional `SkyDirection` at `csp.BeamsConfiguration.field`.
* Class related to receptor grouping, pointing and trajectory were moved into a new `receptorgroup` module. Classes
  related to projection and trajectory were renamed for brevity and consistency, and to reflect that they are not
  specific to Holography. Change are:
  - `core.TrajectoryConfig` renamed to `receptorgroup.Trajectory`
  - `core.HolographyPattern` renamed to `receptorgroup.TrajectoryType`
  - `core.MosaicTrajectoryConfig` renamed to `receptorgroup.MosaicTrajectory`
  - `core.TableTrajectoryConfig` renamed to `receptorgroup.TableTrajectory`
  - `core.FixedTrajectoryConfig` renamed to `receptorgroup.FixedTrajectory`
  - Trajectory `attrs` classes refactored to be child classes of the associated `Trajectory`.
    - `core.MosaicAttrsConfig` -> `receptorgroup.MosaicTrajectory.Attrs`
    - `core.TableAttrsConfig` -> `receptorgroup.TableTrajectory.Attrs`
    - new: `receptorgroup.FixedTrajectory.Attrs`
  - `core.HolographyReceptorGroupConfig` renamed to `receptorgroup.ReceptorGroup`
  - `core.ProjectionConfig` renamed to `receptorgroup.Projection`
  - `core.ProjectionName` rename to `receptorgroup.ProjectionType`
  - `core.ProjectionAlignment` rename to `receptorgroup.ProjectionAlignment`

## 12.3.1
* Data model changes to support ADR-99:
  - Updated MidCBFConfiguration default None for frequency_band_offset_stream1, frequency_band_offset_stream2 and correlation.

## 12.3.0
* Data Model changes to support Holography as per ADR-106
  - Configure schema updated for Holography as per ADR-106
  - Groups key added in pointing configuration
  - In this release validation added only for mosaic, table, fixed pattern
  - Adds HolographyReceptorGroupConfig , TrajectoryConfig and ProjectionConfig to subarray_node/configuration
  - Adds MosaicTrajectoryConfig, TableTrajectoryConfig, FixedTrajectoryConfig to support for Table, Mosaic and Fixed pattern

## 12.2.0
* Data model changes to support ADR-99:
  - Deprecated csp.FSPConfiguration
  - Deprecated csp.CBFConfiguration
  - Adds new MidCBFConfiguration.

## 12.1.0
* Integrated latest OSD version into CDM.
* After integration of OSD due to newly added semantic validation rules
  few assign and scan testcases were failing so fixed those.

## 12.0.0
* Updated default schema for sdp-configure to 0.4
* Added a default schema for sdp-assignres to 0.4
* **BREAKING** Removed depreciated kwargs for SDPConfiguration in central_node/sdp.py

## 11.0.1
* Updated default schema URIs for LOW assign resources and configure
* Adds static type checking with Pyright to python-lint pipeline.
* Adds custom serialiser to CdmObject to exclude default None, [] and {} from JSON output.

## 11.0.0
* **BREAKING** provided support to LOW assign/configure schema with interface 4.0.
* Modified mccs block and added new csp block with pss/pst support for LOW assign resource schema.
* Added pst block in LOW configure schema.

## 10.1.2
* Fixes check for partial configuration to exclude SpecialTarget class object.
* Adds field validators to assure subarray_id in range 1-16, inclusive.

## 10.1.1
* Removes PLUTO as an allowed target_name for SpecialTarget().

## 10.1.0
* Adds subarray_node.configure.core.SpecialTarget() to represent nonsidereal targets.
* Adds custom serialiser to CdmObject to exclude default None, [] and {} from JSON output.

## 10.0.0
* Removes Marshmallow schemas.
* CDM models are no longer @dataclasses, but Pydantic BaseModel subclasses.
* **BREAKING** All CDM models now require keyword arguments.
* Semantic validations only run when strictness is 2 or higher.

## 9.2.1
* OSD Patch release integration

## 9.2.0
* Integrated new OSD release into CDM..
* Consumed semantic validation from OSD.

## 9.1.1
* BTN-2332 - Updated the make submodule, Updated RtD Theme and added Changelog to RtD

## 9.1.0
* BTN-2265 - Added ability to apply, maintain or reset a previously calculated reference pointing calibration

## 9.0.0
* Utilised ska_telmodel v1.15.1 with OSO-TMC low configure schema 3.2
* Created class for low cbf VIS station beams configurations
* SAH-1500 - Update low delay model calculation to accept Ra-Dec in configure command
* CT-1244 - Support other teams
* Updated existing unit tests and add new tests

## 8.3.0
* Updated version of ska_telmodel which has first (early) version of Observatory Static Data (OSD)
*  Added semantic validation support for SBD

## 8.2.0
* Updated version of ska_telmodel which has semantic validation for SBD
* Added new rule, next line support and modified frequency min max ranges in
  existing semantic validation test-cases.
* Added default schema to AssignResourcesRequest, ReleaseResourcesRequest and
  ConfigureRequest

## 8.1.0
* Added PI-20 low schema support
* Added semantic validation support for PI-20 low schema

## 8.0.1
* Fixes an AttributeError when SKA_TELMODEL_SOURCES not set

## 8.0.0
* Support for TMC.partial_configuration and Target offset parameters
* All classes in ska_tmc_cdm.messages are now Python dataclasses with
  Pydantic validation. This will enforce runtime type-checking that may
  break callers passing invalid types

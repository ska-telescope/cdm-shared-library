
============================================
Semantic Validation of Mid & Low Telescope
============================================


Semantic Validation
-------------------

It referred to as a semantic error. It is generally encountered at run time. 
It occurs when a statement is syntactically valid but semantically invalid. 
This type of error is tough to catch.
To catch this type of error we have created a framework named 'Semantic Validation'
into 'ska_telmodel' under 'telvalidation' package and integrated the same into 'CDM'.

To do the Semantic Validation of received JSON for any other component through CDM 
there are some steps which user needs to follow.

* Step 1
   Add latest CDM version into 'pyproject.toml' file.
   
* Step 2
   Import ``semantic_validate_schema`` function from ‘ska-tmc-cdm’ jsonschema classes

   .. code-block:: python
      
      from ska_tmc_cdm.jsonschema.json_schema.JsonSchema import semantic_validate_schema  

* Step 3
   If developer wants to go with semantic validation then he needs to call
   'semantic_validate_schema' function which is present under jsonschema class of 'ska_tmc_cdm'
   and provide appropriate parameters to the function. There are two parameters for this function
   which are 'instance' & 'uri'.
   'instance' is a dictionary which user wants to validate
   and 'uri' is a string containing interface of schema.
   If json is against AA0.5 complaince then it will throw the 'SchematicValidationError'
   exception. 

   .. code-block:: python

      try:
         return semantic_validate_schema(
            instance: dict, 
            uri: str
         )

      except SchematicValidationError as exc:
            raise exc
    

   Import 'SchematicValidationError' from 'ska_telmodel' which contains all the customized error messages
   in string format.

   .. code-block:: python

      from ska_telmodel.telvalidation.semantic_validator import SchematicValidationError   
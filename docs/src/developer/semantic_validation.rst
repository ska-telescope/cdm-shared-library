
====================================
Semantic Validation of Mid Telescope
====================================


Semantic Validation
-------------------

It referred to as a semantic error. It is generally encountered at run time. 
It occurs when a statement is syntactically valid but does not do what the 
programmer intended. This type of error is tough to catch.
To catch this type of error we have created a framework named ``Semantic Validation``
into ``ska_telmodel`` and integrated the same into ``CDM``.

There are some steps to integrate this framework these are as follows:

* Step 1
   Here we have created ``semantic_validate_json`` function in ``shared`` module under 
   ``ValidatingSchema`` class.

   .. code::

    def semantic_validate_json(self, data, process_fn=lambda x: x, **_):
        """
        Validate JSON using the Telescope Model schema.

        The process_fn argument can be used to process semantically correct
        but schematically invalid Python to something equivalent but valid,
        e.g., to convert a list of Python tuples to a list of lists.

        :param data: Marshmallow-provided dict containing parsed object values
        :param process_fn: data processing function called before validation
        """
    
* Step 2
   Called ``semantic_validate_json`` function into ``validate_on_dump`` and 
   ``validate_on_load`` for validating all the parameters.

* Step 3
   This function first checks for interface then call ``semantic_validate_schema`` function
   which we have created in ``json_schema`` module under ``JsonSchema`` class.

   .. code::

    def semantic_validate_schema(instance: dict, uri: str) -> None:
          """
          Validate an instance dictionary under the given schema.

          :param uri:  The schema to validate with
          :param instance: The instance to validate
          :return: None, in case of valid data otherwise, it raises SchematicValidationError exception.
          """
    
* Step 4
   This function reutrns value based on ``televalidation_schema.semantic_validate`` function 
   which we are importing from ska_telmodel repo.
   
   ``from ska_telmodel.telvalidation import semantic_validator as televalidation_schema``

   If semantic validation fails then it will raise ``SchematicValidationError`` error.
   This exception have created in the ska_telmodel repo and importing here.

   ``from ska_telmodel.telvalidation.semantic_validator import SchematicValidationError``

* Step 5
   tm_data object is created and updated true for accessing all files which are 
   loading with TMData in CDM library. 
      
   ``tm_data = TMData(update=True)``


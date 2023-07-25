
====================================
Semantic Validation of Mid Telescope
====================================


Semantic Validation
-------------------

It referred to as a semantic error. It is generally encountered at run time. 
It occurs when a statement is syntactically valid but does not do what the 
programmer intended. This type of error is tough to catch.

  1. Here we have created ``semantic_validate_schema`` function in ``json_schema`` module.

  .. code::

    def semantic_validate_schema(instance: dict, uri: str) -> None:
          """
          Validate an instance dictionary under the given schema.

          :param uri:  The schema to validate with
          :param instance: The instance to validate
          :return: None, in case of valid data otherwise, it raises an exception.
          """
    
  2. This function reutrns value based on ``televalidation_schema.semantic_validate`` function 
     which we are importing from ska_telmodel repo.

     ``from ska_telmodel.telvalidation import semantic_validator as televalidation_schema``

  3. Then we have added ``semantic_validate_json`` function in ``shared`` module under 
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
        :return:
        """
    
  4. tm_data object is created and updated true for accessing "mid-validation-contants.json" 
     in CDM library. 
     
     ``tm_data = TMData(update=True)``

  5. We have created one new flag named ``SEMANTIC_VALIDATE`` which checks for semantic validation.
     If user returns True for semantic validation then it would go for ``semantic_validate_schema`` function.
     
     ``SEMANTIC_VALIDATE = "Run semantic validation"``

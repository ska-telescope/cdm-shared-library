
====================================
Semantic Validation of Mid Telescope
====================================


Semantic Validation
-------------------

It referred to as a semantic error. It is generally encountered at run time. 
It occurs when a statement is syntactically valid but does not do what the 
programmer intended. This type of error is tough to catch.
To catch this type of error we have created a framework named 'Semantic Validation'
into 'ska_telmodel' and integrated the same into 'CDM'.
Currently semantic validation is applicable for two resources: 'assign_resources' and 
'configure' of Mid telescope. It is not applicable for low telescope.

There are some steps to integrate this framework these are as follows:

* Step 1
   Here we have created ``semantic_validate_json`` function in ``shared`` module under 
   ``ValidatingSchema`` class.
   Have created a new flag named ``SEMANTIC_VALIDATE``. Initially we have assigned it False.

   ``SEMANTIC_VALIDATE = "Run semantic schema validation"``

   It is used to check whether user wants to check for semantic validation or not. As of now 
   only two resources are allowed for semantic validation that's why we have assigned it is 
   ``True`` for 'assign_resources' and 'configure'.

   .. code-block:: python

      # for assign_resources
      self.context[ValidatingSchema.SEMANTIC_VALIDATE] = True

      # for configure resources
      self.context[shared.ValidatingSchema.SEMANTIC_VALIDATE] = True

    
* Step 2
   Called ``semantic_validate_json`` function into ``validate_on_dump`` and 
   ``validate_on_load`` for validating all the parameters.

   .. code-block:: python
      
      self.semantic_validate_json(data, process_fn=process_fn)

* Step 3
   This function first checks for interface then call ``semantic_validate_schema`` function
   which we have created in ``json_schema`` module under ``JsonSchema`` class.

    
* Step 4
   This function reutrns value based on ``televalidation_schema.semantic_validate`` function 
   which we are importing from ska_telmodel repo.
   If semantic validation fails then it will raise ``SchematicValidationError`` error.
   This exception have created in the ska_telmodel repo and importing here.

   .. code-block:: python

      # importing semantic_validator module from telvalidation package
      from ska_telmodel.telvalidation import semantic_validator as televalidation_schema

      # importing SchematicValidationError exception to catch errors
      from ska_telmodel.telvalidation.semantic_validator import SchematicValidationError

* Step 5
   Importing TMData from ska_telmodel which is present under data package.
   tm_data object is created and updated true for accessing all files which are 
   loading with TMData in CDM library. 
      
   .. code-block:: python

      # importing TMData from ska_telmodel
      from ska_telmodel.data import TMData

      # creating tm_data object
      tm_data = TMData(update=True)


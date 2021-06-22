.. _`Using the CDM`:

=============
Using the CDM
=============

To use this library in your project, create objects using the classes defined
in ``ska_tmc_cdm.messages`` and convert them to/from JSON using
``ska_tmc_cdm.schemas.CODEC``.

The Python snippet below is an example of constructing a JSON argument for a
``CentralNode.ReleaseResources()`` command. The resulting JSON can be sent to
the device using a ``DeviceProxy``.

.. code-block:: python

  # import the classes for ReleaseResources commands and CODEC for serialisation
  from ska_tmc_cdm.messages import ReleaseResourcesRequest
  from ska_tmc_cdm.schemas import CODEC

  # create an object for a command that will release all resources on subarray #2
  cmd_arg = ReleaseResourcesRequest(2, release_all=True)
  # convert the argument to JSON, ready for use in a DeviceProxy call
  as_json = CODEC.dumps(cmd_arg)

Below is an example of converting the JSON response from a
``CentralNode.AssignResources()`` command to Python objects. The example
assumes you have the string response from the command call at hand.

.. code-block:: python

  # import the classes for ReleaseResources commands and CODEC for serialisation
  from ska_tmc_cdm.messages import AssignResourcesResponse
  from ska_tmc_cdm.schemas import CODEC

  # assume that you have some JSON-formatted string returned by AssignResources()
  json_response = ...
  # convert the JSON to a Python object. This requires you to provide the class
  # you want to convert to
  unmarshalled = CODEC.loads(AssignResourcesResponse, json_response)
  # This object can hold other objects, as defined by the schema. For example,
  # the response for an AssignResources command includes the dish IDs of the
  # dishes that were assigned to it. The schema converts this into a
  # DishAllocation object we can inspect and manipulate
  print(f'Dish IDs allocated: {unmarshalled.dish.receptor_ids}')

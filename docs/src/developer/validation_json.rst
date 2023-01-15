.. _`CDM Library Integration steps for validating JSON schema in Central Node`:

==================================================
Validating JSON schema through CDM in Central Node
==================================================

‘ska-tmc-cdm’ validation/serialisation library contains message and
schema classes for several commands of CentralNode , SubArrayNode of
both mid and low telescope. The classes for message provide the way to
create Python object for the requested command with correct attributes
that comes from a JSON string which must contain just the right keys and
their valid values. This input JSON is first validated in the classes
for schema and then passed to constructor of message class for finally
creating object. Further the CDM extends the ‘Telescope Model’ which
should contain all logical checks related to the validity of attribute
values for a given command.

The whole purpose of maintaining all the classes for message and schema
at CDM is so that other TMC interfaces can communicate with all TANGO
devices without requiring to validate by its own the available JSON.
Otherwise there will be duplicacy of logic as well as hard time
maintaining the different components by different teams working
internationally.

Here we shall see one such example, where Central Node shall use CDM to
validate the received JSON string for release resources request
replacing its local validation.

**Steps**

1. Import from ‘ska-tmc-cdm’ message classes for the command here
ReleaseResources as well as CODEC from schemas in following way

.. code-block:: python

    # for mid telescope
    from ska_tmc_cdm.messages.central_node.release_resources import
    (
        ReleaseResourcesRequest,
    )
    # for low telescope
    from ska_tmc_cdm.messages.mccscontroller.releaseresources import
    (
        ReleaseResourcesRequest as ReleaseResourcesRequestLow,
    )

# CODEC provides the loads and dumps methods for converting JSON
String—>Python object and vice versa for classes defined in
ska_tmc_cdm.message

.. code-block:: python

    from ska_tmc_cdm.schemas import CODEC

2. Find the appropriate place where currently the JSON string is being
validated and result code, error message is being returned.

In this example, for release resources we found one validate_input_json
method in release_resources_command.py.

.. code-block:: python

    try:
        # created python dictionary parsing from input json string
        jsonArgument = json.loads(argin)
    except Exception as e:
        # ResultCode Failed and custom error message
        ...
    # all validations here and if all success then
    return ResultCode.OK, ""

3. Changes to be considered :

i. As we saw during import there are two seperate message classes -
**one for mid telescope and other for low telescope** so we would
require **two validate methods in place of one**.

ii. Replace **json.loads->**\ **CODEC.loads within try block** and **any
error message** should **come from CDM** **extending Telescope Model**
if request JSON is invalid for the command be it by syntax or logical.

iii. For the time being some validations which are not been checked at
CDM and/or Telescope Model need to be done within else block of try.
Finally code snippet should look like:

.. code-block:: python

    try:
        # creation of cdm object from input json argin.
        release_request = CODEC.loads(ReleaseResourcesRequest, argin)
    except Exception as excep:
        # return ResultCode Failed and exception message
        ...
    else:
        # remaining custom local validation
        ...

        # if no error occurred
        return ResultCode.OK, ""

**Scenarios for unit tests**

We can only be sure that this approach worked by writing unit-tests
where we see ResultCode to be Ok and successfully requested object gets
created when our JSON input is valid. In other case, three error
scenarios we have tried for mid-telescope release resource to verify the
message is indeed appropriate and comes from CDM :

Test scenario 1: JSON is missing (a mandatory key) sub array id.

Test scenario 2: The input JSON has misspelt ‘release_all’ key as
‘releaseall’ – invalid key error.

Test scenario 3: The input JSON string has provided number to
‘release_all’ key which takes either True/False - invalid value error.

**Resources**

1. A proof of concept for replacing custom JSON validation for commands
in Central Node (above) can be found at
https://gitlab.com/ska-telescope/ska-tmc/ska-tmc-centralnode/-/tree/nak-75-replacing-customjsonparsing-cdmobj.

2. Central Node is a coordinator of the complete Telescope Monitoring
and Control (TMC) system. Find ska-tmc-centralnode repository at
https://gitlab.com/ska-telescope/ska-tmc/ska-tmc-centralnode.

3. SKA Control Data Model provides Python/JSON serialisation for the
command arguments for various TMC interfaces with other subsystems. Find
ska-tmc-cdm repository at https://gitlab.com/ska-telescope/ska-tmc-cdm/

4. SKA Telescope Model is a dynamic computational model to answer all
queries about the state of the Telescope. Find this library at
https://gitlab.com/ska-telescope/ska-telmodel
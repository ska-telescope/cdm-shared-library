.. _`Integration Steps for Expand and Contract Design Pattern in CDM for Tango Command Interfaces`:

=========================================
Expand and Contract Design Pattern in CDM
=========================================

Every PI as we gradually evolve we expect schemas to keep changing as
well, some scenarios like - commands may take new keywords in addition
to / or replacing existing ones; there may be change in what kind of
input a keyword takes in different schemas etc.

Thus devices and helper libraries would need to support an
expand/contract strategy so that devices and JSON schemas could evolve
without breaking compatibility with older clients. During expand, all
required version of schemas should be supported, but users are expected
to migrate to using the latest one as soon as possible. There may never
be a final schema since as observatory evolves the science more
information may need to be communicated from start to end. However, we
will certainly like to discontinue many older schemas from time to time.
This will be the contract phase

Since CDM validation/serialisation library should be used to validate
the JSON strings for several commands of CentralNode , SubArrayNode and
hence we start there by showing how commands through CDM will support
the strategy with particular example of ‘release resources’.

**Supporting existing and upcoming schemas with new keys in expand phase**


We need to modify two message classes and two schema classes of release
resource for both mid (central_node) and low (mccscontroller) telescopes
respectively.

We can think of two scenarios that we need to support. Let’s understand
the required modifications step by step for each scenario with example
of a dummy schema for mid-telescope release resources.

**Scenario 1 :** Small number of additional unique keys and the values
that they may take is well understood.

.. code-block:: 

	{
	 <existing keys> ...
	 "sdp_id": "sbi-mvp01-20220919-00001", # new in this schema
	 "sdp_max_length": 125.40, # new in this schema
	}

**Steps:**

1. In constructor of the message class for <command>(here
ReleaseResourcesRequest), add new parameters and declare them None
value.

.. code-block:: python
     
     def __init__(
          self,
          interface: str = None,
          transaction_id: str = None,
          subarray_id: int = None,
          release_all: bool = False,
          dish_allocation: Optional[DishAllocation] = None,
          sdp_id: str = None,
          sdp_max_length: float = None,
          ):
          # init existing keys
          ...
          self.sdp_id = sdp_id
          self.sdp_max_length = sdp_max_length
     
          # value errors
          ...


2. Inside @post_load of schema class for <command> (here
‘ReleaseResourcesRequestSchema’), we modify for the same new keys as
added in messages

.. code-block:: python

     @post_load
	def create_request(self, data, **_):
		..
		sdp_id = data.get("sdp_id", None) 
		sdp_max_length = data.get("sdp_max_length", None)

	     return ReleaseResourcesRequest(
		...
		sdp_id=sdp_id,
		sdp_max_length=sdp_max_length,
	     )


3. We need to add the new keys otherwise unknown field validation error
would be raised.

.. code-block:: python

	class ReleaseResourcesRequestSchema(ValidatingSchema):
	# known fields
		...
		sdp_id = fields.String()
		sdp_max_length = fields.Float()

**Scenario 2 :** While supporting multiple schemas the number of unique
keys across several versions of schemas has grown very large and their
validation is maintained at Telescope Model and/or the values they take
is different across schemas.

1. In constructor of the message class for <command>(here
ReleaseResourcesRequest), add \**kwargs. We would also want to mention
in constructor explicitly only those parameters which we’re sure and/or
very important like we want to raise value error for incorrect value etc
, rest let pass through kwargs.

2. In the body of constructor we need to add one line,

.. code-block:: python

     self.__dict__.update(kwargs)


Finally the code snippet should look like:-

.. code-block:: python

     def __init__(
          self,
          *_, # force non-keyword args
          interface: str = None,
          transaction_id: str = None,
          subarray_id: int = None,
          release_all: bool = False,
          dish_allocation: Optional[DishAllocation] = None,
          sdp_id: str = None,
          sdp_max_length: float = None,
          **kwargs, # arbitary keyword-value pairs
          ):
          # init existing keys
          ...
          self.sdp_id = sdp_id
          self.sdp_max_length = sdp_max_length
          
          # update new keywords-value pairs.
          self.__dict__.update(kwargs)
          
          # value errors
          ...


3. Inside @post_load of schema class for <command> (here
‘ReleaseResourcesRequestSchema’), we modify to allow all keys to come.

.. code-block:: python

     @post_load
     def create_request(self, data, **_):
          return ReleaseResourcesRequest(**data, )


4. However there is an additional challenge that validation error may
get raised since the new keys are not mentioned inside schema class for
<command>. For this we can propose the following :

i. including unknown in class Meta found in the same file. This would
pass validation and work with load. But if we dump from object to JSON
string these keys on the fly won’t be there. To have them working in
both load and dump it seems we need to explicitly know atleast the keys
and mention as additional.

.. code-block:: python

     class Meta:
          unknown = INCLUDE # passes validation and load but dump won't show these keys
          additional=('subbands','dummy_key1',) # mention all such expected keys


ii. Since CDM extends Telescope Model we can expect Telescope Model to
maintain all keys and accepted values for validation to pass anyway.

**Expectations in Contract phase**

There should be additional challenges in contract phase that will be
understood as we evolve. However for now we expect to:

i.   Remove support of kwargs

ii.  Mention all keys by hand for the final schema.

iii. Have logical default values instead of declaring with NonelNull
     values. Remove null filtering in schemas.

     Users should not get away without correct keys and valid values in
     contract phase.

**How to use during expand phase**

from ska_tmc_cdm.schemas import CODEC

*1. If we have some JSON-formatted string release_input_str*

.. code-block:: 

     {
      "interface":"https://schema.skao.int/ska-tmc-releaseresources/2.0",
      "transaction_id":"txn-....-00001",
      "subarray_id":1,
      "release_all":true,
      "receptor_ids":[],
      "sdp_max_length": 125.40, # new key but mentioned in message, schema classes
      "subbands": [0.55e9, 0.95e9, 186], # on the fly
      "dummy_key1":"val1" # on the fly
     }

# Convert the JSON to a Python object

.. code-block:: python

     req=CODEC.loads(ReleaseResourcesRequest, release_input_str) # requested object


*2. If we received the object and want to convert it to JSON which may
be used in a DeviceProxy call*

.. code-block:: python

     json_str=CODEC.dumps(req) # from object to JSON string


3. Inside @post_load of schema class for <command> (here
‘ReleaseResourcesRequestSchema’) we expect the same message class
constructor ‘ReleaseResourcesRequest’ to be able to support across
different schemas using kwargs.

.. code-block:: python

     # expand
     request = ReleaseResourcesRequest(
          transaction_id="tma1",
          subarray_id=1,
          dish_allocation=DishAllocation(receptor_ids=["ac", "b", "aab"]),
          sdp_id="sbi-mvp01-20220919-00001", # new in this schema
          sdp_max_length=125.40, # new in this schema
          subbands=[0.55e9, 0.95e9, 186], # arbitary new key-value captured
          release_all=False,
          )
     # contract
     request = ReleaseResourcesRequest(
          transaction_id="tma1",
          subarray_id=1,
          dish_allocation=DishAllocation(receptor_ids=["ac", "b", "aab"]),
          sdp_id="sbi-mvp01-20220919-00001", # new in this schema
          )


**Resources**

1. A prototype can be found at
https://gitlab.com/ska-telescope/ska-tmc-cdm/-/tree/nak-74-expand-contract-design-pattern.

2. Dummy schema for mid telescope release resource.
   
.. code-block:: 

     {
      "interface": https://schema.skao.int/ska-tmc-releaseresources/2.2, #optional
      "subarray_id": 1,
      "release_all": False,
      "receptor_ids": ["ac", "b", "aab"],
      "sdp_id": "sbi-mvp01-20220919-00001", # new in this schema
      "sdp_max_length": 125.40, # new in this schema
      "subbands: [0.55e9, 0.95e9, 186] # arbitary new key-value captured by kwargs​
     }

3. Dummy schema for low telescope release resource.

.. code-block:: 

     {
      "interface": https://schema.skao.int/ska-tmc-releaseresources/2.2, #optional
      "subarray_id": 1,
      "release_all": False,
      "subarray_beam_ids": [3], # new in this schema
      "channels": [[3, 4]], # new in this schema
     }

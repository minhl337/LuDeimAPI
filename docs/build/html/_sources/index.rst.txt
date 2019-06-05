.. LuDeimAPI documentation master file, created by
   sphinx-quickstart on Tue Jun  4 16:20:31 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the LuDeimAPI documentation
======================================

LuDeimAPI is a JSON-RPC 2.0 compliant api designed for use in the LuDeim diamond supply chain management system. The api has a companion API called LuDeimStorageAPI which handles the storage and retrieval of non-trivial size objects within the system. This documentation will not go over this companion API as it is not intended to be called directly from a front-end application.

JSON-RPC 2.0
============

LuDeimAPI is a fully JSON-RPC 2.0 compliant api. The full JSON-RPC 2.0 specification can be found here_. It's only a few pages and very readable. It is highly recommended that anyone looking to develop on top of LuDeimAPI read that document. However, for those that don't, here's the skinny:

* All requests must be formatted in the following way.

.. code-block:: javascript

   {
      "jsonrpc": "2.0",
      "method": NAME_OF_METHOD_BEING_CALLED,
      "params": OBJECT_CONTAINING_THE_REQUIRED_PARAMETERS,
      "id": ID_NUMBER_FOR_THE_REQUEST
   }

* Every response will come in one of the following formats. If the method executed without errors:

.. code-block:: javascript

   {
      "jsonrpc": "2.0",
      "result": OBJECT_CONTAINING_THE_RESULT_OF_YOUR_CALL,
      "id": ID_NUMBER_OF_THE_CORRESPONDING_REQUEST
   }

If the method execution threw an error:

.. code-block:: javascript

   {
      "jsonrpc": "2.0",
      "error": {
         "code": ERROR_CODE,
         "message": ERROR_MESSAGE
      },
      "id": ID_NUMBER_OF_THE_CORRESPONDING_REQUEST
   }

* All requests should be sent to the **/api/** endpoint.

Sessions
========

LuDeimAPI sessions are persistent. That is if you are logged in you will stay logged in until you either clear your cache or the server running LuDeimAPI is restarted. To clear your session, call the **logout** method.

As a convenience, your account's **uuid** and **type** are stored in your server session whenever **login** is called. As a result, once **login** has been called the uuid field of all requests can be safely omitted.

Additionally, the contents of the current session can be returned by calling **get_sess**, and arbitrary string key-value pairs can be added to the session via the **put_sess**. Note that if **put_sess** is called with a key-value pair whose key is already defined in the session, then the value for that key will get overwritten with the new one.

Batch Requests
==============

One large feature of the JSON-RPC 2.0 standard is batch requests. Batch requests allow multiple request objects to be sent in as a single request. This is done by adding all the individual request objects to a list, and sending that list as your request object. For instance:

.. code-block:: javascript

   [
      {
         "jsonrpc": "2.0",
         "method": "foo",
         "params": [
            1,
            2,
            3
         ],
         "id": 1
      },
      {
         "jsonrpc": "2.0",
         "method": "bar",
         "params": {
            "arg1": "james",
            "arg2": "kim",
            "arg3": "chris"
         },
         "id": 2
      },
      {
         "jsonrpc": "2.0",
         "method": "other_thing",
         "params": true,
         "id": 3
      }
   ]

This has a few benefits. First, the number of requests that can be grouped in this way is unbounded. So, if you want to make an extremely large number of requests all at once, then this is a great way to reduce the networking overhead associated with doing that. Also, Batch requests are defined as being unordered. That is, the order in which request objects are included in the list doesn't determine the order in which the server executes them. This may seem like a bad thing, but it allows the server to run batch requests asynchronously which can drastically reduce the time required to compute a response. There is a side effects to this asynchronous behavior though. Sessions are read and updated independently for each request. This means session behavior for batch requests is quite unpredictable. The best course of action is to not use batch requests with methods that interact with the session.

User Types
==========

* mining_company

* distributor

* jeweler

Location Types
==============

* mine

* warehouse

* store

Method: add_user
====================
**PERMISSION LEVEL**
   * public

**ARGUMENTS**
   * **username:** string
   * **password_hash:** string
   * **type:** string

**ARGUMENT CONSTRAINTS**
   * The username must be between 8 and 64 characters
   * The password_hash must be between 64 and 128 characters
   * The type must be one of the valid types defined in the *User Types* section of this document

**RESPONSE MEMBERS**
   * **uuid:** string
   * **type:** string

**RESPONSE MEMBERS MEANING**
   * The uuid returned is the uuid associated with the new user created by the method call. It is required to make any changes to that user's various attributes.
   * The type is the same as the type that was sent in as an argument. It can safely be ignored or used in a continuation function.

**EXAMPLE REQUEST**
   .. code-block:: javascript

      {
         "jsonrpc": "2.0",
         "method": "add_user",
         "params": {
            "type": "mining_company",
            "username": "abcdefghijk",
            "password_hash": "abcdefghabcdefghabcdefghabcdefghabcdefghabcdefghabcdefghabcdefgh"
         },
         "id": 1
      }

**EXAMPLE SUCCESSFUL RESPONSE**
   .. code-block:: javascript

      {
         "jsonrpc": "2.0",
         "result": {
            "uuid": "813ebc3dcc3798a3f6ec9ea24d104f401362c6b6c5ed8032a78b643fd9afe502",
            "type": "mining_company"
         },
         "id": 1
      }

.. _here: https://www.jsonrpc.org/specification

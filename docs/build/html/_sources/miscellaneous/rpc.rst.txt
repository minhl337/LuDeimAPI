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

.. _here: https://www.jsonrpc.org/specification
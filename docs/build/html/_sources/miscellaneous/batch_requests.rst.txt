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
Get Session
===========

**METHOD NAME**
    *get_sess*

**PERMISSION LEVEL**
    *user*

**ARGUMENTS**
    * No arguments, just send **{}**

**RESPONSE MEMBERS**
    * This method returns your current server session object as a dictionary.

**EXAMPLE REQUEST**
    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "get_sess",
            "params": {},
            "id": 1
        }

**EXAMPLE SUCCESSFUL RESPONSE**
    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": {
                "key1": "value1",
                "key2": "value2",
                "key3": "value3"
            },
            "id": 1
        }

**NOTES**
    This method should be called when a user wants to retrieve information they've stored in their session. This method can, of course, only be called when logged.
Logout
======

**METHOD NAME**
    *login*

**PERMISSION LEVEL**
    *user*

**ARGUMENTS**
    * There are no arguments to this method. Just send *{}* as your params object.

**RESPONSE MEMBERS**
    * Response is just the boolean, *True*.

**EXAMPLE REQUEST**
    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "logout",
            "params": {},
            "id": 1
        }

**EXAMPLE SUCCESSFUL RESPONSE**
    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": true,
            "id": 1
        }
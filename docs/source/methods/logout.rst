Logout
======

**METHOD NAME**
    *logout*

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

**NOTES**
    This method should be called when a user wants to end leave the site. This method removes the user's *uuid* and *type* from their session. Should a user want to auto-login the next time they visit the site this method should simply not be called upon leaving which will result in the server remembering the user the next time they visit the site. Whether a user is login can be checked via the **get_sess** method.
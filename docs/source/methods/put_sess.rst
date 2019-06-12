Put Session
===========

**METHOD NAME**
    *put_sess*

**PERMISSION LEVEL**
    *user*

**ARGUMENTS**
    * **key:** string
    * **value:** string

**RESPONSE MEMBERS**
    * This method just returns **True** indicating the key-value pair has been added to your session.

**EXAMPLE REQUEST**
    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "put_sess",
            "params": {
                "key": "MY_KEY",
                "value": "MY_VALUE"
            },
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
    This method should be called when a user wants to save information in their session. While sessions are persistent they should NOT be considered permanent storage.
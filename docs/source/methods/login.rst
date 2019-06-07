Login
=====

**METHOD NAME**
    *login*

**PERMISSION LEVEL**
    *public*

**ARGUMENTS**
    * **username:** string
    * **password_hash:** string

**ARGUMENT CONSTRAINTS**
    * The username must be between 8 and 64 characters
    * The password_hash must be between 64 and 128 characters

**RESPONSE MEMBERS**
    * **uuid:** string
    * **type:** string

**RESPONSE MEMBERS MEANING**
    * The uuid returned is the uuid associated with the user logged in by the method call. It is required to make any changes to that user's various attributes.
    * The type is the same as the type is the type of the user being logged in by the method call. Use this to display different website pages based on the type of the user that is logged in.

**EXAMPLE REQUEST**
    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "login",
            "params": {
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

**NOTES**
    This method should be called when a user tries to login. While many methods can be called without being logged in via an optional *uuid* argument, this is discouraged. The intended use is to call the login method whenever a user logs into the frontend then not have to worry about providing a uuid for each request. Login will fail if the user tries logging in with a non-existent account. This should be expected and caught by the frontend.
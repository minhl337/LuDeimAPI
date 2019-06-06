Add User
========

**METHOD NAME**
    *add_user*

**PERMISSION LEVEL**
    *public*

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
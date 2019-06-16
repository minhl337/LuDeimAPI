Add User
========

:strong:`Method Name:` :literal:`add_user`

:strong:`Permission Level:` |lit_public|_

:strong:`Argumentation:`

    * **username** *(string)* -- This should be your username.

    * **password_hash** *(string)* -- This should be a hash of the password. The algorithm used to form the hash is up the front end. SHA256 is recommended.

    * **type** *(string)* -- This is the type of user you want to create. It must be a |lit_user_type|_.

:strong:`Response Members:`

    * **uuid:** *(string)* -- The new user's |lit_UUID|_ which is required to make user level permissioned request. Defined as SHA256(CONCAT(username, password_hash)).

    * **type:** *(string)* -- The |lit_user_type|_ of the of user created.

:strong:`Example Request:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "add_user",
            "params": {
                "username": "joe.bloggs",
                "password_hash": "2B678F9EFE22C8E57336C4997CBF3923AB6B6B82C37AD041F6773C22D11AEDE9",
                "type": "mining_company"
            },
            "id": 1
        }

:strong:`Example Response:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": {
                "uuid": "ED905886F16EE7733E02EFADB3C95E2EC4B36CBB5511DACD76909BB513BA8E56",
                "type": "mining_company"
            },
            "id": 1
        }

:strong:`Notes`

    This method is intended to be used when creating a new user. Keep in mind that all users must have different usernames. An error will be returned in this case.

.. |lit_user_type| replace:: :literal:`user type`
.. |lit_public| replace:: :literal:`public`
.. |lit_UUID| replace:: :literal:`UUID`

.. _lit_user_type: ../constants/user_types.html
.. _lit_public: ../miscellaneous/permissions.html
.. _lit_UUID: ../constants/uuids.html

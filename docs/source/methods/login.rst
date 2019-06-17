Login
=====

:strong:`Method Name:` :literal:`login`

:strong:`Permission Level:` |lit_public|_

:strong:`Argumentation:`

    * **username:** *(string)* -- The username of the user logging in.

    * **password_hash:** *(string)* -- The hash of the user logging in. The hash must be done using the same algorithm used when signing up.

:strong:`Response Members:`

    * **user_id:** *(string)* -- The new user's |lit_user_id|_ which is required to make user level permissioned request. Defined as SHA256(CONCAT(username, password_hash)).

    * **type:** *(string)* -- The |lit_type|_ of the of user created.

:strong:`Example Request:`

    Find out about the assumptions made when writing this example code, here_.

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "add_location",
            "params": {
                "username": "joe.bloggs",
                "password_hash": "2B678F9EFE22C8E57336C4997CBF3923AB6B6B82C37AD041F6773C22D11AEDE9"
            },
            "id": 1
        }

:strong:`Example Response:`

    Find out about the assumptions made when writing this example code, here_.

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

    This method is intended to be used when logging into an existing user. The login method is really just adding the user's |lit_user_id|_ and |lit_type|_ to the server session. Think of this method as a wrapper for a few |func_put_sess|_ calls.

:strong:`Example Assumptions`

    .. _here:

    The examples above require an assumption to make sense. They assume the user sending the request exists in the system already.

.. |lit_public| replace:: :literal:`user`
.. |lit_user_id| replace:: :literal:`user_id`
.. |lit_type| replace:: :literal:`type`
.. |func_put_sess| replace:: :func:`put_sess`

.. _lit_public: ../miscellaneous/permissions.html
.. _lit_user_id: ../constants/uuids.html
.. _lit_type: ../constants/user_types.html
.. _func_put_sess: ../methods/put_sess.html

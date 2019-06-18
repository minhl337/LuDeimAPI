Change Username
===============

:strong:`Method Name:` :literal:`change_username`

:strong:`Permission Level:` |lit_user|_

:strong:`Argumentation Schemes:`

    * **user_id** *(string)* |lit_conditionally_optional|_  -- When changing your username you may either call |func_login|_ and then omit any arguments to this method or not call |func_login|_ and instead send your |lit_user_id|_ as an argument to this method.

    * **new_username** *(string)* -- This is the new username you'd like to use.

:strong:`Response Members:`

    * **new_user_id** *(string)* -- This is your new user_id. You have a new user_id because your user_is dependent on your username. So, changing your username changes your user_id. As a convenience this new user_id is also updated in your session.

:strong:`Example Request:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "change_username",
            "params": {
                "new_username": "joe.bloggs",
            },
            "id": 1
        }

:strong:`Example Response:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": {
                "new_user_id": "62213BEEAE522D1A5582CBE0AAAB301ED2A757F5E9DEF9F6C9833FC60C5A3589"
            },
            "id": 1
        }

.. |lit_conditionally_optional| replace:: :literal:`conditionally optional`
.. |lit_user| replace:: :literal:`user`
.. |lit_user_id| replace:: :literal:`user_id`

.. |func_login| replace:: :func:`login`
.. |func_get_user_locations| replace:: :func:`get_user_locations`

.. _lit_conditionally_optional: ../miscellaneous/optional_arguments.html
.. _lit_user: ../miscellaneous/permissions.html
.. _lit_user_id: ../constants/uuids.html

.. _func_login: ../methods/login.html
.. _func_get_user_locations: ../methods/get_user_locations.html
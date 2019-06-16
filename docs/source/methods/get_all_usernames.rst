Get All Usernames
=================

:strong:`Method Name:` :literal:`get_all_usernames`

:strong:`Permission Level:` |lit_public|_

:strong:`Argumentation:`

    This method takes no arguments. Just send an empty dictionary, :code:`{ }`.

:strong:`Response Members:`

    This method returns a list of usernames.

:strong:`Example Request:`

    Find out about the assumptions made when writing this example code, here_.

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "get_all_usernames",
            "params": { },
            "id": 1
        }

:strong:`Example Response:`

    Find out about the assumptions made when writing this example code, here_.

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": [
                "johnny1234",
                "1998wildride",
                "username1234"
            ],
            "id": 1
        }

:strong:`Notes`

    This method is intended to be used to get a list of all the users in the system.

:strong:`Example Assumptions`

    .. _here:

    The examples above require an assumption to make sense. They assume the user sending the request is logged in.

.. |lit_public| replace:: :literal:`user`

.. _lit_public: ../miscellaneous/permissions.html

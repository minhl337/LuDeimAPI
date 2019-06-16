Logout
======

:strong:`Method Name:` :literal:`logout`

:strong:`Permission Level:` |lit_user|_

:strong:`Argumentation:`

        This method takes no arguments. Just send an empty dictionary, :code:`{ }`.

:strong:`Response Members:`

    This method returns the boolean :code:`true` upon success.

:strong:`Example Request:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "logout",
            "params": { },
            "id": 1
        }

:strong:`Example Response:`

    Find out about the assumptions made when writing this example code, here_.

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": true,
            "id": 1
        }

:strong:`Example Assumptions`

    .. _here:

    The examples above require an assumption to make sense. They assume the user sending the request is logged in to begin with. Logging out while not logged in will return an error.

.. |lit_user| replace:: :literal:`user`

.. _lit_user: ../miscellaneous/permissions.html

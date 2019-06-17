Get Session
===========

:strong:`Method Name:` :literal:`get_sess`

:strong:`Permission Level:` |lit_public|_

:strong:`Argumentation:`

    This method takes no arguments. Just send an empty dictionary, :code:`{ }`.

:strong:`Response Members:`

    This method returns your server session as string-to-string dictionary.

:strong:`Example Request:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "get_sess",
            "params": { },
            "id": 1
        }

:strong:`Example Response:`

    Find out about the assumptions made when writing this example code, here_.

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": {
                "user_id": "ED905886F16EE7733E02EFADB3C95E2EC4B36CBB5511DACD76909BB513BA8E56",
                "type": "mining_company",
                "abcd": "lmnop"
            }
            "id": 1
        }

:strong:`Example Assumptions`

    .. _here:

    The examples above require an assumption that the user is logged in, and at some point put the key-value pair "abcd" - "lmnop" into their server session.

.. |lit_public| replace:: :literal:`user`

.. _lit_public: ../miscellaneous/permissions.html

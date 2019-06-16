Put Session
============

:strong:`Method Name:` :literal:`put_sess`

:strong:`Permission Level:` |lit_public|_

:strong:`Argumentation:`

    * **key:** *(string)* -- This is the key for the value being stored in your server session.

    * **value:** *(string)* -- This is the value being stored in your server session.

:strong:`Response Members:`

    This method returns the boolean :code:`true` upon success.

:strong:`Example Request:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "put_sess",
            "params": {
                "key": "abcd",
                "value": "lmnop"
            },
            "id": 1
        }

:strong:`Example Response:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": true,
            "id": 1
        }

:strong:`Notes`

    This method is intended to be used as an arbitrary key-value store. However, it only supports strings. If you want to store other types you will have to serialize them and deserialize them before sending them in.

.. |lit_public| replace:: :literal:`public`

.. _lit_public: ../miscellaneous/permissions.html

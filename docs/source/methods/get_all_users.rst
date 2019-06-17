Get All Users
=================

:strong:`Method Name:` :literal:`get_all_users`

:strong:`Permission Level:` |lit_public|_

:strong:`Argumentation:`

    This method takes no arguments. Just send an empty dictionary, :code:`{ }`.

:strong:`Response Members:`

    This method returns a list of partial users objects. These partial user objects can be thought of as anonymized user objects. The user's password_hash and user_id are both omitted.

:strong:`Example Request:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "get_all_users",
            "params": { },
            "id": 1
        }

:strong:`Example Response:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": [
                {
                    "username": "johnny1234",
                    "uuid": "ED905886F16EE7733E02EFADB3C95E2EC4B36CBB5511DACD76909BB513BA8E56",
                    "location_uuids": [],
                    "item_uuids": [],
                    "avatar": "link_to_avatar_image",
                    "type": "mining_company"
                },
                {
                    "username": "1998wildride",
                    "uuid": "18EE24150DCB1D96752A4D6DD0F20DFD8BA8C38527E40AA8509B7ADECF78F9C6",
                    "location_uuids": [
                        "C387880FA02DFFE80E2A9883CB767BB57465F40FA82FEB03EC5403124E672E56",
                        "50A19EB20FA7FE4A9B3C36AAC95EFC6EB4F8D93BADA9802CAEC2D30222043217"
                    ],
                    "item_uuids": [
                        "80BA56A70AB0C1E0CDA97FE0726316ADA61D0EA55259B6954C8644F20B3C786A",
                        "93BB9E6F403FA04D6101DEB920DC224916B2D9B55D33E05773DFEC075CB24AE3"
                    ],
                    "avatar": "link_to_maybe_a_different_avatar_image",
                    "type": "jeweler"
                }

                "username1234"
            ],
            "id": 1
        }

:strong:`Notes`

    This method is intended to be used to get a list of all the users in the system.

.. |lit_public| replace:: :literal:`user`

.. _lit_public: ../miscellaneous/permissions.html

Get User Items
==============

:strong:`Method Name:` :literal:`get_user_locations`

:strong:`Permission Level:` |lit_public|_

:strong:`Argumentation Schemes:`

    .. admonition:: Argumentation Scheme 1

        * **username** *(string)* -- When looking up another user's items use this argumentation scheme using their username as the argument.

    .. admonition:: Argumentation Scheme 2

        * **user_id** *(string)* |lit_conditionally_optional|_  -- When looking up your own items you may either call |func_login|_ and then omit any arguments to this method or not call |func_login|_ and instead send your |lit_user_id|_ as an argument to this method.

:strong:`Response Members:`

        This method returns a list of item objects. If no location items were found for the requested user, then the list will be empty. However, if the user being looked up simply doesn't exist, then the method will return an error rather than an empty list.

        Item objects are fairly self explanatory except for the user_uuids and location_uuids. If the item's status is stationary the last user uuid in the user_uuids list is the uuid of the current owner of the item and the last location uuid in the location_uuids list is the uuid of the current location of the item. However, if the item's status is transit, then the item owner is the second to last uuid in the user_uuid list and the last user uuid in the user_uuids list signifies the user who will take ownership if the transfer is accepted. Additionally, if the item is in transit the last location uuid in the location_uuids list is the destination of the item while the second to last item is the source location's uuid.

:strong:`Example Request:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "get_user_items",
            "params": {
                "username": "joe.bloggs"
            },
            "id": 1
        }

:strong:`Example Response:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": [
                {
                    "uuid": "CA0AEC8C35E27B62DB4A27ACED44E13B7C97BD715D0E5029A06491CC7C2A2200CA0AEC8C35E27B62DB4A27ACED44E13B7C97BD715D0E5029A06491CC7C2A2200",
                    "type": "mine",
                    "location_uuids": [
                        "300F1FB5953602D6B49BCD34762B0BD26B519C057465499217CB337ED5512651",
                        "9DFA3179431258A0E49786E8BDED7307A84814950877B77A55B9C2AC71CB15B5",
                        "BD9C36C69E4ACCF91842B08C5D86BF5C3F1E1C78860387BD15718AC7CEE8C67D"
                    ],
                    "user_uuids": [
                        "4C6843BF44357EE0FBD09437B1515B11CEF997413409D730B2DD55076903471D",
                        "CAAB7A1F0AF72B3AE3B955EEC51F9FF1B9AF752681C3CB7757B29AEB7D051034",
                        "7B24455245FF3F6EE891C4FC6232CB78EFC47EB770F72CDFC3A194FBEE929EB0"
                    ],
                    "status": "stationary"
                }
            ],
            "id": 1
        }

.. |lit_conditionally_optional| replace:: :literal:`conditionally optional`
.. |lit_public| replace:: :literal:`public`
.. |lit_user_id| replace:: :literal:`user_id`

.. |func_login| replace:: :func:`login`

.. _lit_conditionally_optional: ../miscellaneous/optional_arguments.html
.. _lit_public: ../miscellaneous/permissions.html
.. _lit_user_id: ../constants/uuids.html

.. _func_login: ../methods/login.html

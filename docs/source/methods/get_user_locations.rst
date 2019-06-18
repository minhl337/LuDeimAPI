Get User Locations
==================

:strong:`Method Name:` :literal:`get_user_locations`

:strong:`Permission Level:` |lit_public|_

:strong:`Argumentation Schemes:`

    .. admonition:: Argumentation Scheme 1

        * **username** *(string)* -- When looking up another user's locations use this argumentation scheme using their username as the argument.

    .. admonition:: Argumentation Scheme 2

        * **user_id** *(string)* |lit_conditionally_optional|_  -- When looking up your own locations you may either call |func_login|_ and then omit any arguments to this method or not call |func_login|_ and instead send your |lit_user_id|_ as an argument to this method.

:strong:`Response Members:`

    This method returns a list of location objects. Look at the example response to see all the location object fields, but they're pretty self explanatory.

:strong:`Example Request:`

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "get_user_locations",
            "params": {
                "username": "joe.bloggs",
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
                    "user_uuids": [
                        "4C6843BF44357EE0FBD09437B1515B11CEF997413409D730B2DD55076903471D4C6843BF44357EE0FBD09437B1515B11CEF997413409D730B2DD55076903471D",
                        "CAAB7A1F0AF72B3AE3B955EEC51F9FF1B9AF752681C3CB7757B29AEB7D051034CAAB7A1F0AF72B3AE3B955EEC51F9FF1B9AF752681C3CB7757B29AEB7D051034",
                        "7B24455245FF3F6EE891C4FC6232CB78EFC47EB770F72CDFC3A194FBEE929EB07B24455245FF3F6EE891C4FC6232CB78EFC47EB770F72CDFC3A194FBEE929EB0"
                    ],
                    "item_uuids": [
                        "300F1FB5953602D6B49BCD34762B0BD26B519C057465499217CB337ED5512651300F1FB5953602D6B49BCD34762B0BD26B519C057465499217CB337ED5512651",
                        "9DFA3179431258A0E49786E8BDED7307A84814950877B77A55B9C2AC71CB15B59DFA3179431258A0E49786E8BDED7307A84814950877B77A55B9C2AC71CB15B5",
                        "BD9C36C69E4ACCF91842B08C5D86BF5C3F1E1C78860387BD15718AC7CEE8C67DBD9C36C69E4ACCF91842B08C5D86BF5C3F1E1C78860387BD15718AC7CEE8C67D"
                    ],
                    "name": "awesome mine",
                    "address": "6325 rocky road, MN, USA",
                    "latitude": 23.4,
                    "longitude": 34.2,
                    "details": "take the back road because of the flooding...",
                    "photo": "https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwiC7LjBw_PiAhUEQ60KHZEkBiEQjRx6BAgBEAU&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FQuarry&psig=AOvVaw2p8nx9vvxiKmJuBEXRncwI&ust=1560964354646034",
                    "representative": {
                        "title": "MR",
                        "first_name": "john",
                        "last_name": "doe",
                        "contact_info": "+1 (123) 456 7890"
                    },
                    "id": 1
                },
                {
                    "uuid": "AB1D83852FC0B76C1A167B72C88AA41646A46FB9793A0D38342D6E3A913ADEDAAB1D83852FC0B76C1A167B72C88AA41646A46FB9793A0D38342D6E3A913ADEDA",
                    "type": "mine",
                    "user_uuids": [
                        "1D833117D6790FD7706070B3CE8349E974C90C87E60A9465FDC887F49A1532061D833117D6790FD7706070B3CE8349E974C90C87E60A9465FDC887F49A153206",
                        "7B24455245FF3F6EE891C4FC6232CB78EFC47EB770F72CDFC3A194FBEE929EB07B24455245FF3F6EE891C4FC6232CB78EFC47EB770F72CDFC3A194FBEE929EB0"
                    ],
                    "item_uuids": [ ],
                    "name": "okay mine",
                    "address": "5679 main st, CA, USA",
                    "latitude": 22.4,
                    "longitude": 64.2,
                    "details": "",
                    "photo": "https://www.pitandquarry.com/wp-content/uploads/2018/10/SEMO-Quarry-Delta-Cos_Inventory-Management.jpg",
                    "representative": {
                        "title": "MR",
                        "first_name": "andrew",
                        "last_name": "smith",
                        "contact_info": "+1 (142) 498 1986"
                    },
                    "id": 1
                }
            ],
            "id": 1
        }

.. |lit_conditionally_optional| replace:: :literal:`conditionally optional`
.. |lit_public| replace:: :literal:`public`
.. |lit_user_id| replace:: :literal:`user_id`

.. |func_login| replace:: :func:`login`
.. |func_get_user_locations| replace:: :func:`get_user_locations`

.. _lit_conditionally_optional: ../miscellaneous/optional_arguments.html
.. _lit_public: ../miscellaneous/permissions.html
.. _lit_user_id: ../constants/uuids.html

.. _func_login: ../methods/login.html
.. _func_get_user_locations: ../methods/get_user_locations.html
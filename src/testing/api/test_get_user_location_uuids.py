import unittest
import reset
import random
import string
import json
import utils.ludeim_constants as lconst
import utils.ludeim_generic_helpers as ludeim
import time
import app


endpoint = "/api/"


class TestApiMethodGetUserLocationUUIDS(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()

    def test__get_user_location_uuids__valid(self):
        time.sleep(1)
        print("\ntest__get_user_location_uuids__valid")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            _type_1 = random.choice(lconst.USER_TYPES)
            username_1 = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_USERNAME_LEN, lconst.MAX_USERNAME_LEN)
                )
            ])
            password_hash_1 = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                )
            ])
            derived_uuid_1 = ludeim.generate_user_uuid(username_1, password_hash_1)
            payload = {
                "jsonrpc": "2.0",
                "method": "add_user",
                "params": {
                    "type": _type_1,
                    "username": username_1,
                    "password_hash": password_hash_1
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
            for i in range(10):
                _type = random.choice(lconst.LOCATION_TYPES)
                name = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(
                        random.randint(5, 50)  # TODO: formalize bounds for location names
                    )
                ])
                address = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(
                        random.randint(5, 50)  # TODO: formalize bounds for addresses
                    )
                ])
                latitude = float(random.randint(1, 360) / random.randint(1, 360))  # TODO: formalize bounds for latitude
                longitude = float(random.randint(1, 360) / random.randint(1, 360))  # TODO: formalize bounds for longitude
                details = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(
                        random.randint(0, 100)  # TODO: formalize bounds for details
                    )
                ])
                rep_title = random.choice(lconst.TITLES)
                rep_first_name = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(
                        random.randint(5, 20)  # TODO: formalize bounds for first names
                    )
                ])
                rep_last_name = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(
                        random.randint(5, 20)  # TODO: formalize bounds for last names
                    )
                ])
                rep_contact_info = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(
                        random.randint(5, 20)  # TODO: formalize bounds for contact info
                    )
                ])
                payload = {
                    "jsonrpc": "2.0",
                    "method": "add_location",
                    "params": {
                        "uuid": derived_uuid_1,
                        "type": _type,
                        "name": name,
                        "address": address,
                        "latitude": latitude,
                        "longitude": longitude,
                        "details": details,
                        "representative": {
                            "title": rep_title,
                            "first_name": rep_first_name,
                            "last_name": rep_last_name,
                            "contact_info": rep_contact_info
                        }
                    },
                    "id": 1
                }
                resp = self.app.post(endpoint, json=payload)
            payload = {
                "jsonrpc": "2.0",
                "method": "get_user_location_uuids",
                "params": {
                    "username": username_1
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            self.assertEqual(len(json.loads(resp.data.decode("utf-8"))["result"]),
                             10,
                             "api response was incorrect")
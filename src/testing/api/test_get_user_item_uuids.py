import unittest
import reset
import random
import string
import json
import utils.ludeim_constants as lconst
import utils.ludeim_generic_helpers as ludeim
import time
import app
import logging
import testing.utils.logging as l


endpoint = "/api/"


class TestApiMethodGetUserItemUUIDS(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()
        logging.basicConfig(level=logging.NOTSET)
        dbg = logging.getLogger('dbg')
        dbg.setLevel(logging.DEBUG)
        self.dbg = dbg
        flask_logger = logging.getLogger('flask')
        flask_logger.setLevel(logging.CRITICAL)

    def test__get_user_item_uuids__valid(self):
        l.log(self.dbg, "entering: test__get_user_location_uuids__valid")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            # NOTE: adding a user
            l.log(self.dbg, "\tadding a user")
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
            derived_user_id_1 = ludeim.generate_user_user_id(username_1, password_hash_1)
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
            # NOTE: logging in
            l.log(self.dbg, "\tlogging in")
            payload = {
                "jsonrpc": "2.0",
                "method": "login_user",
                "params": {
                    "username": username_1,
                    "password_hash": password_hash_1
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
            # NOTE: adding a location
            l.log(self.dbg, "\tadding a location")
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
            self.app.post(endpoint, json=payload)
            # NOTE: getting the location's uuid
            l.log(self.dbg, "\tgetting the location's uuid")
            payload = {
                "jsonrpc": "2.0",
                "method": "get_user_location_uuids",
                "params": {
                    "username": username_1
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            resp = resp.json
            # NOTE: adding a few items
            l.log(self.dbg, "\tadding a few items")
            for _ in range(10):
                payload = {
                    "jsonrpc": "2.0",
                    "method": "add_item",
                    "params": {
                        "location_uuid": resp["result"][0]
                    },
                    "id": 1
                }
                self.app.post(endpoint, json=payload)
            # NOTE: looking up all the item uuids
            l.log(self.dbg, "\tlooking up the item uuids")
            payload = {
                "jsonrpc": "2.0",
                "method": "get_user_item_uuids",
                "params": {
                    "username": username_1
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            resp = resp.json
            l.log(self.dbg, "\tasserting the correct number of items were made")
            self.assertIn("result", resp, "response was an error")
            self.assertEqual(10, len(resp["result"]), "incorrect number of items returned")
            l.log(self.dbg, "\tending round {}\n".format(_))


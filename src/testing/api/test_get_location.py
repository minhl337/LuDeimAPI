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


class TestApiMethodGetLocation(unittest.TestCase):
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

    def test__get_location__valid(self):
        l.log(self.dbg, "entering: test__get_location__valid")
        for _ in range(10):  # NOTE: run 100 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tresetting the application")
            self.setUp()  # NOTE: reset client to prevent carry over sessions
            l.log(self.dbg, "\tadding a user")
            # NOTE: adding a user
            _type = random.choice(lconst.USER_TYPES)
            username = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_USERNAME_LEN, lconst.MAX_USERNAME_LEN)
                )
            ])
            password_hash = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                )
            ])
            derived_user_id = ludeim.generate_user_user_id(username, password_hash)
            payload = {
                "jsonrpc": "2.0",
                "method": "add_user",
                "params": {
                    "type": _type,
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
            # NOTE: login to the user
            l.log(self.dbg, "\tlogging into the user")
            payload = {
                "jsonrpc": "2.0",
                "method": "login_user",
                "params": {
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
            # NOTE: add a location to that user
            l.log(self.dbg, "\tadding a location to the user")
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
            # NOTE: look up the user's location uuids
            l.log(self.dbg, "\tlooking up the user's location uuids")
            payload = {
                "jsonrpc": "2.0",
                "method": "get_user_location_uuids",
                "params": {},
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            loc_uuid = resp.json["result"][0]
            # NOTE: look up the location based on uuid and compared to expected
            l.log(self.dbg, "\tlooking up the location based on the uuid")
            payload = {
                "jsonrpc": "2.0",
                "method": "get_location",
                "params": {
                    "location_uuid": loc_uuid
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            l.log(self.dbg, "\tasserting the response is not an error")
            self.assertIn("result", resp.json, "returned no error")
            l.log(self.dbg, "\tending round {}\n".format(_))

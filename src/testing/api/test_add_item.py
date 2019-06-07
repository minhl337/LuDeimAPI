import unittest
import reset
import random
import string
import json
import utils.ludeim_constants as lconst
import utils.response_constants as rconst
import utils.ludeim_generic_helpers as ludeim
import utils.database_helpers as db
import app
import logging
import time
import multiprocessing
import os
from gevent import monkey
monkey.patch_all()  # NOTE: needed due to dependency problems with grequests (must be above grequests import)
import grequests


endpoint = "/api/"


class TestApiMethodAddItem(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()

    def test__add_item__valid__with_uuid(self):
        time.sleep(1)
        print("\ntest__add_item__valid__with_uuid")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            # NOTE: add a new user
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
            derived_uuid = ludeim.generate_user_uuid(username_1, password_hash_1)
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
            # NOTE: login to the new user
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username_1,
                    "password_hash": password_hash_1
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
            # NOTE: add a location to that new user
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
                    "uuid": derived_uuid,
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
            # NOTE: get the user's location's uuid
            payload = {
                "jsonrpc": "2.0",
                "method": "get_user_location_uuids",
                "params": {
                    "username": username_1
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            resp = json.loads(resp.data.decode("utf-8"))
            # NOTE: add an item to the new user at this location
            payload = {
                "jsonrpc": "2.0",
                "method": "add_item",
                "params": {
                    "location_uuid": resp["result"][0]
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            resp = json.loads(resp.data.decode("utf-8"))
            db_dump = db.get_connection().execute("""SELECT * FROM items""").fetchall()
            self.assertEqual(len(db_dump), 1, "database didn't update correctly")
            self.assertEqual(db_dump[0][1:],
                             (lconst.DIAMOND,
                              json.dumps((payload["params"]["location_uuid"],)),
                              json.dumps((derived_uuid,))),
                             "database didn't update correctly")
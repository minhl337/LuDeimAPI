import unittest
import reset
import random
import string
import utils.database_helpers as db
import utils.ludeim_constants as lconst
import utils.ludeim_generic_helpers as ludeim
import json
import app
import logging
import testing.utils.logging as l


endpoint = "/api/"


class TestApiMethodBeginTransfer(unittest.TestCase):
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

    def test__begin_transfer__valid(self):
        l.log(self.dbg, "entering: test__begin_transfer__valid")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tresetting the application")
            self.setUp()  # NOTE: reset client to prevent carry over sessions
            l.log(self.dbg, "\tadding a user")
            # NOTE: adding user 1
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
            resp = self.app.post(endpoint, json=payload)
            # NOTE: adding user 2
            l.log(self.dbg, "\tadding a second user")
            _type_2 = random.choice(lconst.USER_TYPES)
            username_2 = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_USERNAME_LEN, lconst.MAX_USERNAME_LEN)
                )
            ])
            password_hash_2 = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                )
            ])
            derived_user_id_2 = ludeim.generate_user_user_id(username_2, password_hash_2)
            payload = {
                "jsonrpc": "2.0",
                "method": "add_user",
                "params": {
                    "type": _type_2,
                    "username": username_2,
                    "password_hash": password_hash_2
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            # NOTE: login to user 1
            l.log(self.dbg, "\tlogging into the first user")
            payload = {
                "jsonrpc": "2.0",
                "method": "login_user",
                "params": {
                    "username": username_1,
                    "password_hash": password_hash_1
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            # NOTE: add a location to user 1
            l.log(self.dbg, "\tadding a location to the first user")
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
                    "user_id": derived_user_id_1,
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
            # NOTE: add a location to user 2
            l.log(self.dbg, "\tadding a location to user 2")
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
                    "user_id": derived_user_id_2,
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
            l.log(self.dbg, "\tlooking up user 1's location's uuid")
            # NOTE: look up user 1's location's uuid
            payload = {
                "jsonrpc": "2.0",
                "method": "get_user_location_uuids",
                "params": {},
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            loc_uuid_1 = resp.json["result"][0]
            l.log(self.dbg, "\tadding a and item to user user 1 at it's only location")
            # NOTE: add an item
            payload = {
                "jsonrpc": "2.0",
                "method": "add_item",
                "params": {
                    "location_uuid": loc_uuid_1
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            l.log(self.dbg, "\tlooking up the item's uuid")
            # NOTE: look up the item's uuid
            payload = {
                "jsonrpc": "2.0",
                "method": "get_user_item_uuids",
                "params": {},
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            item_uuid = resp.json["result"][0]
            l.log(self.dbg, "\tlooking up user 2's location uuids")
            # NOTE: look up user 2's location's uuid
            payload = {
                "jsonrpc": "2.0",
                "method": "get_user_location_uuids",
                "params": {
                    "username": username_2
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            loc_uuid_2 = resp.json["result"][0]
            # NOTE: get all users
            payload = {
                "jsonrpc": "2.0",
                "method": "get_all_users",
                "params": { },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            for user in resp.json["result"]:
                if user["username"] == username_2:
                    dest_uuid_2 = user["uuid"]
            # NOTE: begin transfer
            l.log(self.dbg, "\tbeginning transfer from user 1's location to user 2's location")
            payload = {
                "jsonrpc": "2.0",
                "method": "begin_transfer",
                "params": {
                    "item_uuid": item_uuid,
                    "destination_location_uuid": loc_uuid_2,
                    "destination_user_uuid": dest_uuid_2
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            l.log(self.dbg, "\tasserting that the transfer has begun")
            self.assertIn("result", resp.json, "result was an error")
            l.log(self.dbg, "\tending round {}\n".format(_))

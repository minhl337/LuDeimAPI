import unittest
import reset
import random
import string
import utils.database_helpers as db
import utils.ludeim_constants as lconst
import utils.ludeim_generic_helpers as ludeim
import time
import app


endpoint = "/api/"


class TestApiMethodBeginTransfer(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()

    def test__begin_transfer__valid(self):
        time.sleep(1)
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            self.setUp()  # NOTE: reset API
            # print("- - - - - - - - - - - - - - - - - - -")
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
            resp = self.app.post(endpoint, json=payload)
            # print("adding user 1: " + str(resp.json))
            # NOTE: adding user 2
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
            derived_uuid_2 = ludeim.generate_user_uuid(username_2, password_hash_2)
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
            # print("adding user 2: " + str(resp.json))
            # NOTE: login to user 1
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username_1,
                    "password_hash": password_hash_1
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            # print("login to user 1: " + str(resp.json))
            # NOTE: add a location to user 1
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
            # print("add location to user 1: " + str(resp.json))
            # NOTE: add a location to user 2
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
                    "uuid": derived_uuid_2,
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
            # print("add location to user 2: " + str(resp.json))
            # NOTE: look up user 1's location's uuid
            payload = {
                "jsonrpc": "2.0",
                "method": "get_user_location_uuids",
                "params": {},
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            # print("look up user 1's locations: " + str(resp.json))
            loc_uuid_1 = resp.json["result"][0]
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
            # print("add an item to user 1: " + str(resp.json))
            # NOTE: look up the item's uuid
            payload = {
                "jsonrpc": "2.0",
                "method": "get_user_item_uuids",
                "params": {},
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            # print("look up user 1's item: " + str(resp.json))
            item_uuid = resp.json["result"][0]
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
            # print("look up user 2's locations: " + str(resp.json))
            loc_uuid_2 = resp.json["result"][0]
            # with self.app as c:
            #     with c.session_transaction() as sess:
            #         print("user1 uuid: " + derived_uuid_1)
            #         print("user2 uuid: " + derived_uuid_2)
            #         print("session: " + str(sess.get("uuid", None)))
            # for x in db.get_connection().execute("""SELECT * FROM users""").fetchall():
            #     print(x)
            # NOTE: begin transfer
            payload = {
                "jsonrpc": "2.0",
                "method": "begin_transfer",
                "params": {
                    "item_uuid": item_uuid,
                    "destination_location_uuid": loc_uuid_2,
                    "destination_user_uuid": derived_uuid_2
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            self.assertIn("result", resp.json, "result was an error")

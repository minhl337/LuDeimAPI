import unittest
import reset
import random
import string
import json
import utils.ludeim_constants as lconst
import utils.response_constants as rconst
import utils.ludeim_generic_helpers as ludeim
import utils.database_helpers as db
import logging
import time
import multiprocessing
import twisted
import os
from gevent import monkey
monkey.patch_all()  # NOTE: needed due to dependency problems with grequests (must be above grequests import)
from requests_threads import AsyncSession
import app


endpoint = "/api/"


class TestApiMethodAddLocation(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()

    def test__add_location__valid__with_uuid(self):
        time.sleep(1)
        print("\ntest__add_location__valid__with_uuid")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
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
            derived_uuid = ludeim.generate_user_uuid(username, password_hash)
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
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "result": True,
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            db_dump = db.get_connection().execute("""SELECT * FROM locations""").fetchall()
            self.assertEqual(len(db_dump), 1, "database didn't update correctly")
            self.assertEqual(db_dump[0][1:-1],
                             (_type, json.dumps([derived_uuid]), '[]', name, address, latitude, longitude, details,
                              lconst.DEFAULT_LOCATION_AVATAR),
                             "database didn't update correctly")
            self.assertEqual(json.loads(db_dump[0][-1]),
                             payload["params"]["representative"],
                             "saved representative incorrect")

    def test__add_location__valid__without_uuid(self):
        time.sleep(1)
        print("\ntest__add_location__valid__without_uuid")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            # NOTE: add a new user
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
            derived_uuid = ludeim.generate_user_uuid(username, password_hash)
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
            # NOTE: login to the new user
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
            # NOTE: add a location to the new user & validate that it worked
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
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "result": True,
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            db_dump = db.get_connection().execute("""SELECT * FROM locations""").fetchall()
            self.assertEqual(len(db_dump), 1, "database didn't update correctly")
            self.assertEqual(db_dump[0][1:-1],
                             (_type, json.dumps([derived_uuid]), '[]', name, address, latitude, longitude, details,
                              lconst.DEFAULT_LOCATION_AVATAR),
                             "database didn't update correctly")
            self.assertEqual(json.loads(db_dump[0][-1]),
                             payload["params"]["representative"],
                             "saved representative incorrect")

    def test__add_location__valid__batch_with_uuid(self):
        time.sleep(1)
        print("\ntest__add_location__valid__batch_with_uuid")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
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
            derived_uuid = ludeim.generate_user_uuid(username, password_hash)
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
            payloads = []
            expected_results = []
            for i in range(25):
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
                    "id": i
                }
                expected_results.append(True)
                payloads.append(payload)
            resp = self.app.post(endpoint, json=payloads)
            resps = json.loads(resp.data.decode("utf-8"))
            for r in resps:
                self.assertIn("result", r, "error response")
                self.assertEqual(r["result"], expected_results[r["id"]], "differing result object")
            db_dump = db.get_connection().execute("""SELECT * FROM locations""").fetchall()
            self.assertEqual(len(db_dump), 25, "database didn't update correctly")

    def test__add_location__valid__batch_without_uuid(self):
        time.sleep(1)
        print("\ntest__add_location__valid__batch_without_uuid")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
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
            derived_uuid = ludeim.generate_user_uuid(username, password_hash)
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
            # NOTE: login to the new user
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
            payloads = []
            for _ in range(25):
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
                longitude = float(
                    random.randint(1, 360) / random.randint(1, 360))  # TODO: formalize bounds for longitude
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
                payloads.append(payload)
            resp = self.app.post(endpoint, json=payloads)
            expected_resp = [
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                }
            ]
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            db_dump = db.get_connection().execute("""SELECT * FROM locations""").fetchall()
            self.assertEqual(len(db_dump), 25, "database didn't update correctly")

    def test__add_location__valid__batch_mixed(self):
        time.sleep(1)
        print("\ntest__add_location__valid__batch_mixed")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
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
            derived_uuid = ludeim.generate_user_uuid(username, password_hash)
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
            # NOTE: login to the new user
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
            payloads = []
            for _ in range(25):
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
                longitude = float(
                    random.randint(1, 360) / random.randint(1, 360))  # TODO: formalize bounds for longitude
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
                if random.randint(0,100) % 2 == 0:
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
                else:
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
                payloads.append(payload)
            resp = self.app.post(endpoint, json=payloads)
            expected_resp = [
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                },
                {
                    "jsonrpc": "2.0",
                    "result": True,
                    "id": 1
                }
            ]
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            db_dump = db.get_connection().execute("""SELECT * FROM locations""").fetchall()
            self.assertEqual(len(db_dump), 25, "database didn't update correctly")

    def test__add_location__valid__async_with_uuid(self):
        time.sleep(1)
        print("\ntest__add_location__valid__async_with_uuid")
        for _ in range(10):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database

            def ex(w):
                os.dup2(w.fileno(), 1)
                app.app.run()
            a, b = multiprocessing.Pipe()
            p = multiprocessing.Process(target=ex, args=(a,))
            log = logging.getLogger('werkzeug')
            log.disabled = True
            p.start()
            time.sleep(2)
            url = "http://" + "127.0.0.1:5000" + endpoint

            session = AsyncSession(n=100)

            async def test():
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
                derived_uuid = ludeim.generate_user_uuid(username, password_hash)
                await (session.post(url=url,
                                         json={
                                             "jsonrpc": "2.0",
                                             "method": "add_user",
                                             "params": {
                                                 "type": _type,
                                                 "username": username,
                                                 "password_hash": password_hash
                                             },
                                             "id": 1
                                         }))
                resps = []
                for _ in range(10):
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
                    latitude = float(
                        random.randint(1, 360) / random.randint(1, 360))  # TODO: formalize bounds for latitude
                    longitude = float(
                        random.randint(1, 360) / random.randint(1, 360))  # TODO: formalize bounds for longitude
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
                    resps.append(session.post(url=url, json=payload))
                for i in range(len(resps)):
                    resps[i] = await resps[i]
                resps = [r.json() for r in resps]
                acc = True
                for r in resps:
                    acc = acc and "result" in r
                self.assertTrue(acc, msg="a request errored")
                db_resp = db.get_connection().execute("""SELECT * FROM locations""").fetchall()
                self.assertEqual(len(db_resp),
                                 10,
                                 "not all locations got saved to the database")
            try:
                session.run(test)
            except twisted.internet.error.ReactorNotRestartable:
                pass
            except SystemExit:  # NOTE: requests_threads is experimental and currently always exits with a hard sys exit
                pass
            p.kill()

    def test__add_location__invalid__type(self):
        time.sleep(1)
        print("\ntest__add_location__invalid__type")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
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
            derived_uuid = ludeim.generate_user_uuid(username, password_hash)
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
            # NOTE: login to the new user
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
            _type = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(50, 100)
                )
            ])
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
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "error": {
                    "code": rconst.INVALID_LOCATION_TYPE_CODE,
                    "message": rconst.INVALID_LOCATION_TYPE
                },
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            db_dump = db.get_connection().execute("""SELECT * FROM locations""").fetchall()
            self.assertEqual(db_dump, [], "database response was incorrect")

    def test__add_location__invalid__representative_title(self):
        time.sleep(1)
        print("\ntest__add_location__invalid__representative_title")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
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
            derived_uuid = ludeim.generate_user_uuid(username, password_hash)
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
            # NOTE: login to the new user
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
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
            rep_title = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(50, 100)
                )
            ])
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
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "error": {
                    "code": rconst.INVALID_REPRESENTATIVE_TITLE_CODE,
                    "message": rconst.INVALID_REPRESENTATIVE_TITLE
                },
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            db_dump = db.get_connection().execute("""SELECT * FROM locations""").fetchall()
            self.assertEqual(db_dump, [], "database inadvertently updated")
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


endpoint = "/api/"


class TestApiMethodAddLocation(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()

    def test__add_location__valid__with_uuid(self):
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
                             (_type, json.dumps([derived_uuid]), name, address, latitude, longitude, details,
                              lconst.DEFAULT_LOCATION_AVATAR),
                             "database didn't update correctly")
            self.assertEqual(json.loads(db_dump[0][-1]),
                             payload["params"]["representative"],
                             "saved representative incorrect")

    def test__add_location__valid__without_uuid(self):
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
                             (_type, json.dumps([derived_uuid]), name, address, latitude, longitude, details,
                              lconst.DEFAULT_LOCATION_AVATAR),
                             "database didn't update correctly")
            self.assertEqual(json.loads(db_dump[0][-1]),
                             payload["params"]["representative"],
                             "saved representative incorrect")

    def test__add_location__invalid__type(self):
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
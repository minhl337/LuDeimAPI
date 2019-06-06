import unittest
import reset
import random
import string
import time
import utils.ludeim_constants as lconst
import utils.ludeim_generic_helpers as ludeim
import app
import json


endpoint = "/api/"


class TestApiMethodGetSess(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()

    def test__get_sess_valid(self):
        time.sleep(1)
        print("\ntest__get_sess_valid")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            # NOTE: add a user
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
            # NOTE: get the session & validate it
            payload = {
                "jsonrpc": "2.0",
                "method": "get_sess",
                "params": {},
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            expected_result = {
                "uuid": derived_uuid,
                "type": _type
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8"))["result"], expected_result, "returned session didn't match expectation")
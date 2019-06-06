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


class TestApiMethodGetAllUsernames(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()

    def test__get_all_usernames__valid(self):
        time.sleep(1)
        print("\ntest__get_all_usernames__valid")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            usernames = []
            for i in range(25):
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
                usernames.append(username_1)
            payload = {
                "jsonrpc": "2.0",
                "method": "get_all_usernames",
                "params": {},
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            results = json.loads(resp.data.decode("utf-8"))["result"]
            self.assertEqual(len(results), 25, "database and/or api error")
            for r in results:
                self.assertIn(r, usernames, "unknown username returned")

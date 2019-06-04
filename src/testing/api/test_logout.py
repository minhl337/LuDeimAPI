import unittest
import reset
import random
import string
import json
import flask
import time
import utils.ludeim_constants as lconst
import utils.response_constants as rconst
import utils.ludeim_generic_helpers as ludeim
import utils.database_helpers as db
import app


endpoint = "/api/"


class TestApiMethodLogout(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()

    def test__logout__valid__without_uuid(self):
        time.sleep(1)
        print("\ntest__login__valid__without_logout")
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
            payload = {
                "jsonrpc": "2.0",
                "method": "logout",
                "params": {
                    "uuid": derived_uuid
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
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]',)],
                             "database updated inadvertently")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess.get("uuid", None),
                                     None,
                                     "uuid not saved in the session correctly during login")
                    self.assertEqual(sess.get("type", None),
                                     None,
                                     "type not saved in the session correctly during login")
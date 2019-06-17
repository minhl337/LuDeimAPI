import unittest
import reset
import random
import string
import json
import time
import utils.ludeim_constants as lconst
import utils.ludeim_generic_helpers as ludeim
import utils.database_helpers as db
import app
import logging
import testing.utils.logging as l


endpoint = "/api/"


class TestApiMethodLogout(unittest.TestCase):
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

    def test__logout__valid__without_uuid(self):
        l.log(self.dbg, "entering: test__logout__valid__without_uuid")
        for _ in range(10):  # NOTE: run 100 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tadding a user")
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
            # NOTE: login to the new user
            l.log(self.dbg, "\tlogging into the new user")
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
            # NOTE: then logout
            l.log(self.dbg, "\tlogging out")
            payload = {
                "jsonrpc": "2.0",
                "method": "logout",
                "params": {},
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "result": True,
                "id": 1
            }
            l.log(self.dbg, "\tasserting that the logout was successful")
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database updated inadvertently")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess.get("user_id", None),
                                     None,
                                     "user_id not saved in the session correctly during login")
                    self.assertEqual(sess.get("type", None),
                                     None,
                                     "type not saved in the session correctly during login")
            l.log(self.dbg, "\tending round {}\n".format(_))

import unittest
import reset
import random
import string
import utils.ludeim_constants as lconst
import utils.ludeim_generic_helpers as ludeim
import app
import json
import logging
import testing.utils.logging as l


endpoint = "/api/"


class TestApiMethodGetSess(unittest.TestCase):
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

    def test__get_sess_valid(self):
        l.log(self.dbg, "entering: test__get_sess_valid")
        for _ in range(10):  # NOTE: run 100 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            # NOTE: add a user
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
            l.log(self.dbg, "\tlogging in")
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
            # NOTE: get the session & validate it
            l.log(self.dbg, "\tgetting the session")
            payload = {
                "jsonrpc": "2.0",
                "method": "get_sess",
                "params": {},
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            expected_result = {
                "user_id": derived_user_id,
                "type": _type
            }
            l.log(self.dbg, "\tasserting the returned session is correct")
            self.assertEqual(json.loads(resp.data.decode("utf-8"))["result"],
                             expected_result,
                             "returned session didn't match expectation")
            l.log(self.dbg, "\tending round {}\n".format(_))

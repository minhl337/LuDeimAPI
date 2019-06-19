import unittest
import reset
import random
import string
import json
import utils.ludeim_constants as lconst
import utils.ludeim_generic_helpers as ludeim
import app
import logging
import testing.utils.logging as l


endpoint = "/api/"


class TestApiMethodGetAllUsers(unittest.TestCase):
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

    def test__get_all_users__valid(self):
        l.log(self.dbg, "entering: test__get_all_usernames__valid")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tadding 25 users")
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
                derived_user_id = ludeim.generate_user_user_id(username_1, password_hash_1)
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
            l.log(self.dbg, "\tgetting all usernames in the system")
            payload = {
                "jsonrpc": "2.0",
                "method": "get_all_users",
                "params": {
                    "user_id": derived_user_id
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            l.log(self.dbg, "\tasserting all 25 usernames are returned")
            results = json.loads(resp.data.decode("utf-8"))["result"]
            self.assertEqual(len(results), 25, "database and/or api error")
            # TODO: implement replacement test
            # for r in results:
            #     self.assertIn(r, usernames, "unknown username returned")
            l.log(self.dbg, "\tending round {}\n".format(_))

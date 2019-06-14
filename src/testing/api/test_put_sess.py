import unittest
import random
import string
import json
import time
import app
import logging
import testing.utils.logging as l


endpoint = "/api/"


class TestApiMethodPutSess(unittest.TestCase):
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

    def test__put_sess__valid(self):
        l.log(self.dbg, "entering: test__put_sess__valid")
        for _ in range(10):  # NOTE: run 100 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the application")
            self.setUp()  # NOTE: reset client to prevent carry over sessions
            l.log(self.dbg, "\tupdating the session")
            payload = {
                "jsonrpc": "2.0",
                "method": "put_sess",
                "params": {
                    "key": "".join([
                        random.choice(string.ascii_letters + string.digits) for _ in range(128)
                    ]),
                    "value": "".join([
                        random.choice(string.ascii_letters + string.digits) for _ in range(128)
                    ])
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            l.log(self.dbg, "\tasserting session updated correctly")
            self.assertIn("result", json.loads(resp.data.decode("utf-8")), "response was an error")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess.get(payload["params"]["key"], None),
                                     payload["params"]["value"],
                                     "session did not update properly")
            l.log(self.dbg, "\tending round {}\n".format(_))

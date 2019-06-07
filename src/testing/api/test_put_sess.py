import unittest
import random
import string
import json
import time
import app


endpoint = "/api/"


class TestApiMethodPutSess(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()

    def test__put_sess__valid(self):
        time.sleep(1)
        print("\ntest__put_sess_valid")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            self.setUp()  # NOTE: reset the test_client to ensure no carry over sessions
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
            self.assertIn("result", json.loads(resp.data.decode("utf-8")), "response was an error")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess.get(payload["params"]["key"], None),
                                     payload["params"]["value"],
                                     "session did not update properly")

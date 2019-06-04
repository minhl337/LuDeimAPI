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
import logging
import time
import multiprocessing
import os
from gevent import monkey
monkey.patch_all()  # NOTE: needed due to dependency problems with grequests (must be above grequests import)
import grequests


endpoint = "/api/"


class TestApiMethodAddUser(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()

    def test__add_user__valid(self):
        time.sleep(1)
        print("\ntest__add_user__valid")
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
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "result": {
                    "type": _type,
                    "uuid": derived_uuid
                },
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]',)],
                             "database didn't update correctly")

    def test__add_user__valid__async(self):
        time.sleep(1)
        print("\ntest__add_user__valid__async")
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
            # CREDIT: https://stackoverflow.com/questions/9110593/asynchronous-requests-with-python-requests
            def ex_handler(request, exception):
                print("the exception failed. that sucks.")
                print(request)
                print(exception)
            reqs = []
            url = "http://" + "127.0.0.1:5000" + endpoint
            for _ in range(10):
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
                reqs.append(grequests.post(url=url,
                                           data=json.dumps({
                                               "jsonrpc": "2.0",
                                               "method": "add_user",
                                               "params": {
                                                   "type": _type,
                                                   "username": username,
                                                   "password_hash": password_hash
                                               },
                                               "id": 1
                                           })))
            resps = grequests.map(reqs, exception_handler=ex_handler)
            p.kill()
            resps = [r.json() for r in resps]
            acc = True
            for r in resps:
                acc = acc and "result" in r
            self.assertTrue(acc, msg="a request errored")
            db_resp = db.get_connection().execute("""SELECT * FROM users""").fetchall()
            self.assertEqual(len(db_resp),
                             10,
                             "not all users got saved to the database")

    def test__add_user__valid__batch(self):
        time.sleep(1)
        print("\ntest__add_location__valid__batch_with_uuid")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            payloads = []
            expected_resp = []
            for i in range(25):
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
                    "id": i
                }
                payloads.append(payload)
                expected_resp.append({"type": _type, "uuid": derived_uuid})
            resp = self.app.post(endpoint, json=payloads)
            resps = json.loads(resp.data.decode("utf-8"))
            for r in resps:
                self.assertIn("result", r, "error response")
                self.assertEqual(r["result"], expected_resp[r["id"]], "incorrect response result object")
            db_dump = db.get_connection().execute("""SELECT * FROM users""").fetchall()
            self.assertEqual(len(db_dump), 25, "database didn't update correctly")

    def test__add_user__invalid__type(self):
        time.sleep(1)
        print("\ntest__add_user__invalid__type")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            _type = "".join([
                        random.choice(string.ascii_letters + string.digits) for _ in range(100)
                    ])
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
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "error": {
                    "code": rconst.INVALID_USER_TYPE_CODE,
                    "message": rconst.INVALID_USER_TYPE
                },
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [],
                             "database didn't update correctly")

    def test__add_user__invalid__short_username(self):
        time.sleep(1)
        print("\ntest__add_user__invalid__short_username")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            _type = random.choice(lconst.USER_TYPES)
            username = "".join([
                        random.choice(string.ascii_letters + string.digits) for _ in range(
                            random.randint(1, lconst.MIN_USERNAME_LEN-1)
                        )
                    ])
            password_hash = "".join([
                        random.choice(string.ascii_letters + string.digits) for _ in range(
                            random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                        )
                    ])
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
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "error": {
                    "code": rconst.INVALID_USER_USERNAME_CODE,
                    "message": rconst.INVALID_USER_USERNAME
                },
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [],
                             "database didn't update correctly")

    def test__add_user__invalid__long_username(self):
        time.sleep(1)
        print("\ntest__add_user__invalid__long_username")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            _type = random.choice(lconst.USER_TYPES)
            username = "".join([
                        random.choice(string.ascii_letters + string.digits) for _ in range(
                            random.randint(lconst.MAX_USERNAME_LEN+1, 10000)
                        )
                    ])
            password_hash = "".join([
                        random.choice(string.ascii_letters + string.digits) for _ in range(
                            random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                        )
                    ])
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
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "error": {
                    "code": rconst.INVALID_USER_USERNAME_CODE,
                    "message": rconst.INVALID_USER_USERNAME
                },
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [],
                             "database didn't update correctly")

    def test__add_user__invalid__short_password_hash(self):
        time.sleep(1)
        print("\ntest__add_user__invalid__short_password_hash")
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
                            random.randint(0, lconst.MIN_PASSWORD_HASH_LEN-1)
                        )
                    ])
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
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "error": {
                    "code": rconst.INVALID_USER_PASSWORD_HASH_CODE,
                    "message": rconst.INVALID_USER_PASSWORD_HASH
                },
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [],
                             "database didn't update correctly")

    def test__add_user__invalid__long_password_hash(self):
        time.sleep(1)
        print("\ntest__add_user__invalid__long_password_hash")
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
                            random.randint(lconst.MAX_PASSWORD_HASH_LEN+1, 10000)
                        )
                    ])
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
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "error": {
                    "code": rconst.INVALID_USER_PASSWORD_HASH_CODE,
                    "message": rconst.INVALID_USER_PASSWORD_HASH
                },
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [],
                             "database didn't update correctly")

    def test__add_user__invalid__username_collision(self):
        time.sleep(1)
        print("\ntest__add_user__invalid__username_collision")
        for _ in range(100):  # NOTE: run 100 random iterations to for robustness
            reset.auto_reset()  # NOTE: reset the database
            _type_original = random.choice(lconst.USER_TYPES)
            username_original = "".join([
                        random.choice(string.ascii_letters + string.digits) for _ in range(
                            random.randint(lconst.MIN_USERNAME_LEN, lconst.MAX_USERNAME_LEN)
                        )
                    ])
            password_hash_original = "".join([
                        random.choice(string.ascii_letters + string.digits) for _ in range(
                            random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                        )
                    ])
            derived_uuid = ludeim.generate_user_uuid(username_original, password_hash_original)
            payload = {
                "jsonrpc": "2.0",
                "method": "add_user",
                "params": {
                    "type": _type_original,
                    "username": username_original,
                    "password_hash": password_hash_original
                },
                "id": 1
            }
            self.app.post(endpoint, json=payload)
            _type_changed = random.choice(lconst.USER_TYPES)
            password_hash_changed = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                )
            ])
            payload = {
                "jsonrpc": "2.0",
                "method": "add_user",
                "params": {
                    "type": _type_changed,
                    "username": username_original,
                    "password_hash": password_hash_changed
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "error": {
                    "code": rconst.USERNAME_TAKEN_CODE,
                    "message": rconst.USERNAME_TAKEN
                },
                "id": 1
            }
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [(derived_uuid, _type_original, username_original, password_hash_original, lconst.DEFAULT_USER_AVATAR, '[]',)],
                             "database didn't update correctly")

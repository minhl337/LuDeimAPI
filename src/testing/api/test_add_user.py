import unittest
import reset
import random
import string
import json
import utils.ludeim_constants as lconst
import utils.ludeim_generic_helpers as ludeim
import utils.database_helpers as db
import app
import time
import multiprocessing
import os
from gevent import monkey
monkey.patch_all()  # NOTE: needed due to dependency problems with grequests (must be above grequests import)
import grequests
import logging
import testing.utils.logging as l


endpoint = "/api/"


class TestApiMethodAddUser(unittest.TestCase):
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
        urllib_logger = logging.getLogger("urllib3.connectionpool")
        urllib_logger.setLevel(logging.CRITICAL)

    def test__add_user__valid(self):
        l.log(self.dbg, "entering: test__add_user__valid")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
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
            l.log(self.dbg, "\tasserting a user was added")
            self.assertIn("result",
                          resp.json,
                          "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database didn't update correctly")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__add_user__valid__async(self):
        l.log(self.dbg, "entering: test__add_user__valid__async")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tadding 10 users asynchronously")
            def ex(w):
                os.dup2(w.fileno(), 1)
                app.app.run()
            a, b = multiprocessing.Pipe()
            p = multiprocessing.Process(target=ex, args=(a,))
            log = logging.getLogger('werkzeug')
            log.disabled = True
            p.start()
            time.sleep(2)
            # SOURCE: https://stackoverflow.com/questions/9110593/asynchronous-requests-with-python-requests
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
            l.log(self.dbg, "\tasserting all 10 users were made")
            self.assertTrue(acc, msg="a request errored")
            db_resp = db.get_connection().execute("""SELECT * FROM users""").fetchall()
            self.assertEqual(len(db_resp),
                             10,
                             "not all users got saved to the database")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__add_user__valid__batch(self):
        l.log(self.dbg, "entering: test__add_user__valid__batch")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tadding 25 users in a single batch request")
            payloads = []
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
                derived_user_id = ludeim.generate_user_user_id(username, password_hash)
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
            resp = self.app.post(endpoint, json=payloads)
            resps = json.loads(resp.data.decode("utf-8"))
            l.log(self.dbg, "\tasserting all 25 users were made")
            for r in resps:
                self.assertIn("result", r, "error response")
            db_dump = db.get_connection().execute("""SELECT * FROM users""").fetchall()
            self.assertEqual(len(db_dump), 25, "database didn't update correctly")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__add_user__invalid__type(self):
        l.log(self.dbg, "entering: test__add_user__invalid__type")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tadding a user with an invalid type")
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
            l.log(self.dbg, "\tasserting the user wasn't successfully created")
            self.assertIn("error",
                          resp.json,
                          "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [],
                             "database didn't update correctly")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__add_user__invalid__short_username(self):
        l.log(self.dbg, "entering: test__add_user__invalid__short_username")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tadding a user with an invalid username")
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
            l.log(self.dbg, "\tasserting the request failed")
            self.assertIn("error",
                          resp.json,
                          "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [],
                             "database didn't update correctly")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__add_user__invalid__long_username(self):
        l.log(self.dbg, "entering: test__add_user__invalid__long_username")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tadding a user with an invalid username")
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
            l.log(self.dbg, "\tasserting the request failed")
            self.assertIn("error",
                          resp.json,
                          "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [],
                             "database didn't update correctly")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__add_user__invalid__short_password_hash(self):
        l.log(self.dbg, "entering: test__add_user__invalid__short_password_hash")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tadding a user with an invalid password hash")
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
            l.log(self.dbg, "\tasserting the request failed")
            self.assertIn("error",
                             resp.json,
                             "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [],
                             "database didn't update correctly")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__add_user__invalid__long_password_hash(self):
        l.log(self.dbg, "entering: test__add_user__invalid__long_password_hash")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tadding a user with an invalid password hash")
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
            l.log(self.dbg, "\tasserting the request failed")
            self.assertIn("error",
                          resp.json,
                          "api response was incorrect")
            self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
                             [],
                             "database didn't update correctly")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__add_user__invalid__username_collision(self):
        l.log(self.dbg, "entering: test__add_user__invalid__username_collision")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tadding a user")
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
            derived_user_id = ludeim.generate_user_user_id(username_original, password_hash_original)
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
            l.log(self.dbg, "\tadding a user with the same username")
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
            l.log(self.dbg, "\tasserting the request failed")
            self.assertIn("error",
                          resp.json,
                          "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type_original, username_original, password_hash_original, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database didn't update correctly")
            l.log(self.dbg, "\tending round {}\n".format(_))

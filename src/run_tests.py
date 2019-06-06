from testing.api.test_add_user import TestApiMethodAddUser
from testing.api.test_add_location import TestApiMethodAddLocation
from testing.api.test_login import TestApiMethodLogin
from testing.api.test_logout import TestApiMethodLogout
from testing.api.test_get_user_location_uuids import TestApiMethodGetUserLocationUUIDS
from testing.api.test_get_all_usernames import TestApiMethodGetAllUsernames

import unittest


loader = unittest.TestLoader()
suite = unittest.TestSuite()
runner = unittest.TextTestRunner(failfast=True)

# add more tests here
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodAddUser))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodAddLocation))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodLogin))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodLogout))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodGetUserLocationUUIDS))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodGetAllUsernames))

runner.run(suite)

from testing.api.test_add_user import TestApiMethodAddUser
from testing.api.test_add_location import TestApiMethodAddLocation
from testing.api.test_login import TestApiMethodLogin
from testing.api.test_logout import TestApiMethodLogout

import unittest


loader = unittest.TestLoader()
suite = unittest.TestSuite()
runner = unittest.TextTestRunner(failfast=True)

# add more tests here
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodAddUser))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodAddLocation))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodLogin))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodLogout))

runner.run(suite)

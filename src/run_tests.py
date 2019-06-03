from testing.api.test_add_user import TestApiMethodAddUser
from testing.api.test_add_location import TestApiMethodAddLocation
from testing.api.test_login import TestApiMethodLogin

import unittest


loader = unittest.TestLoader()
suite = unittest.TestSuite()
runner = unittest.TextTestRunner(failfast=True)

# add more tests here
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodAddUser))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodAddLocation))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodLogin))

runner.run(suite)
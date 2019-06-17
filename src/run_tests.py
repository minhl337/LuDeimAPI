from testing.api.test_add_user import TestApiMethodAddUser
from testing.api.test_add_location import TestApiMethodAddLocation
from testing.api.test_add_item import TestApiMethodAddItem
from testing.api.test_login import TestApiMethodLogin
from testing.api.test_logout import TestApiMethodLogout
from testing.api.test_get_user_location_uuids import TestApiMethodGetUserLocationUUIDS
from testing.api.test_get_all_users import TestApiMethodGetAllUsers
from testing.api.test_get_sess import TestApiMethodGetSess
from testing.api.test_put_sess import TestApiMethodPutSess
from testing.api.test_get_location import TestApiMethodGetLocation
from testing.api.test_begin_transfer import TestApiMethodBeginTransfer
from testing.api.test_get_user_locations import TestApiMethodGetUserLocations
from testing.api.test_get_user_items import TestApiMethodGetUserItems
from testing.api.test_get_user_item_uuids import TestApiMethodGetUserItemUUIDS


import unittest


loader = unittest.TestLoader()
suite = unittest.TestSuite()
runner = unittest.TextTestRunner(failfast=True)

# add more tests here
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodAddUser))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodAddLocation))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodAddItem))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodLogin))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodLogout))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodGetUserLocationUUIDS))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodGetAllUsers))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodGetSess))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodPutSess))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodGetLocation))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodBeginTransfer))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodGetUserLocations))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodGetUserItems))
suite.addTest(loader.loadTestsFromTestCase(TestApiMethodGetUserItemUUIDS))

runner.run(suite)

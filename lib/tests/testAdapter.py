from sys import argv
from importlib import import_module
import unittest
from .IOs.forAdapterTests import *

from lib.internals.utilities.verification import verifyConfigurations
from lib.internals.utilities.verification import verifyAdapters


# Presteps
## This is needed in order to make it possible to specify the imported adapter from the command line.
## If it is not specified on the command line if will take the configured one in configs.py as default.
if len(argv) == 2:
    adapter = argv[1]
else:
    from conf.configs import adapter

## Verify all needed components for module testing
##
## We verify all configurations
verifyConfigurations()
## We only verify the adapter being tested right now
verifyAdapters(adapter)

## NOTE: We are manually importing the module here and no just importing the package adapters in order to have
## control about which package we import. The adapters module ALWAYS imports the configured adapter, which is not
## always desired.
## Import the module of the configured adapter and make it accessible with the variable adapterModule
adapterModule = import_module("lib.adapters."+adapter)
## Make all attributes of adapterModule directly accessible (Simulation for from <module> import *)
globals().update(
            {n: getattr(adapterModule, n) for n in adapterModule.__all__} if hasattr(adapterModule, '__all__') 
            else 
            {k: v for (k, v) in adapterModule.__dict__.items() if not k.startswith('_')}
          )


# Testing --------------------------------------------------------------------------------------------------------------
## Groups API Tests:
class CreateGroupTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        pass

    def testCreateGroup(self):
        # See if it is possible to create a group
        result = createGroup(CreateGroupTestsIO.inputs["name"])
        # See if the creation actually altred the state of the status site
        self.assertIn(CreateGroupTestsIO.inputs["name"], 
                      map(lambda x: x["name"], readGroups()), 
                      "The group was not returend by the status site after attempted creation")
        # Check the return type of the operation
        self.assertEqual(type(result),
                         CreateGroupTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as defined by the specification")
        # Check whether the required information by the specification is returned
        self.assertTrue(all(key in result for key in CreateGroupTestsIO.outputs["returnedDictKeys"]),
                        "The information required by the specification was not returned")

        # Save the ID as it is needed later for the teardown
        self.createdGroupID = result["ID"]

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created group during the test
        deleteGroup(self.createdGroupID)
            

class ReadGroupsTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create groups to be read in the tests and save their IDs as they are needed later for the teardown.
        self.createdGroupsIDs = []
        for name in ReadGroupsTestsIO.fixture["names"]:
            self.createdGroupsIDs.append(createGroup(name)["ID"])

    def testReadGroups(self):
        # Attempt to read all groups
        result = readGroups()
        # Check the return type
        self.assertEqual(type(result),
                         ReadGroupsTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as required by the specification")
        # Check the type of the child objects as the return type is a container
        self.assertEqual(type(next(iter(result))),
                         ReadGroupsTestsIO.outputs["returnedChildType"],
                         "The return value child doesn't have the correct type, as required by the specification")
        # Check whether the required information by the specification is returned
        for group in result:
            self.assertTrue(all(key in group for key in ReadGroupsTestsIO.outputs["returnedDictKeys"]),
                            "The information required by the specification was not returned")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete all created groups during the tests
        for ID in self.createdGroupsIDs:
            deleteGroup(ID)

class DeleteGroupsTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create a group to test its deletion
        self.createdGroupsIDs = createGroup(DeleteGroupTestsIO.fixture["name"])["ID"]

    def testDeleteGroup(self):
        # Attempt to delete the test group
        deleteGroup(self.createdGroupsIDs)

    # Teardown after EVERY test method
    def tearDown(self):
        pass


## Components API Tests:
class CreateComponentTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        pass

    def testCreateComponent(self):
        # See if it is possible to create a component
        result = createComponent(CreateComponentTestsIO.inputs["component"])
        # See if the creation actually altred the state of the status site
        self.assertIn(CreateComponentTestsIO.inputs["component"]["name"], 
                      map(lambda x: x["name"], readComponents()), 
                      "The component was not returend by the status site after attempted creation")
        # Check the return type of the operation
        self.assertEqual(type(result),
                         CreateComponentTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as defined by the specification")
        # Check whether the required information by the specification is returned
        self.assertTrue(all(key in result for key in CreateComponentTestsIO.outputs["returnedDictKeys"]),
                        "The information required by the specification was not returned")

        # Save the ID as it is needed later for the teardown
        self.createdComponentID = result["ID"]

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created group during the test
        deleteComponent(self.createdComponentID)

class ReadComponentsTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        pass

    # Teardown after EVERY test method
    def tearDown(self):
        pass

class UpdateComponentTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        pass

    # Teardown after EVERY test method
    def tearDown(self):
        pass

class DeleteComponentTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        pass

    # Teardown after EVERY test method
    def tearDown(self):
        pass


## Incidents API Tests:


if __name__ == "__main__":
    # Configuring the executed tests
    ## Here you can turn off individual tests
    GroupsAPITests = unittest.TestSuite()
    GroupsAPITests.addTest(CreateGroupTests("testCreateGroup"))
    GroupsAPITests.addTest(ReadGroupsTests("testReadGroups"))
    GroupsAPITests.addTest(DeleteGroupsTests("testDeleteGroup"))

    ComponentsAPITests = unittest.TestSuite()
    ComponentsAPITests.addTest(CreateComponentTests("testCreateComponent"))

    ## Here you can turn off whole suites
    APITest = unittest.TestSuite()
    APITest.addTest(GroupsAPITests)
    APITest.addTest(ComponentsAPITests)

    # Running the tests
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(APITest)


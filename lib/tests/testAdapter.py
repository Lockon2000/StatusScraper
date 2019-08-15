# Still needed work
# 1. complete the last three tests
# 2. make the tests also check for the dict key types not only their existences



from sys import argv
from importlib import import_module
import unittest
from .IOs.forAdapterTests import *

from lib.internals.utilities.verification import verifyConfigurations
from lib.internals.utilities.verification import verifyAdapters


# Presteps
## This is needed in order to make it possible to specify the tested adapter from the command line.
## If it is not specified on the command line it will take the configured one in configs.py as default.
if len(argv) == 2:
    adapter = argv[1]
else:
    from conf.configs import adapter

## Verify all needed components for module testing
### We verify all configurations
verifyConfigurations()
### We only verify the adapter being tested right now
verifyAdapters(adapter)

## NOTE: We are manually importing the module here and not just importing the package adapters in order to have
## control about which package we import. The adapters package ALWAYS imports the configured adapter, which is not
## always desired.
## Import the module of the configured adapter and make it accessible with the variable adapterModule
adapterModule = import_module("lib.adapters."+adapter)
## Make all attributes of adapterModule directly accessible (Simulation for from <module> import *)
globals().update(
            {n: getattr(adapterModule, n) for n in adapterModule.__all__} if hasattr(adapterModule, '__all__') 
            else 
            {k: v for (k, v) in adapterModule.__dict__.items() if not k.startswith('_')}
          )


# Testing
# ----------------------------------------------------------------------------------------------------------------------
## Groups API Tests:
class CreateGroupTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        pass

    def testCreateGroup(self):
        # Attempt to create a group
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

class ReadGroupTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create a group to be read in the tests and save its ID as its needed later for the teardown.
        self.createdGroupsID = createGroup(ReadGroupTestsIO.fixture["name"])["ID"]

    def testReadGroup(self):
        # Attempt to read the group
        result = readGroup(self.createdGroupsID)
        # Check the return type of the operation
        self.assertEqual(type(result),
                         ReadGroupTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as required by the specification")
        # Check whether the required information by the specification is returned
        self.assertTrue(all(key in result for key in ReadGroupTestsIO.outputs["returnedDictKeys"]),
                        "The information required by the specification was not returned")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created group during the tests
        deleteGroup(self.createdGroupsID)

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
        # Check the return type of the operation
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
        self.createdGroupIDs = createGroup(DeleteGroupTestsIO.fixture["name"])["ID"]

    def testDeleteGroup(self):
        # Attempt to delete the test group
        deleteGroup(self.createdGroupIDs)

    # Teardown after EVERY test method
    def tearDown(self):
        pass


# ----------------------------------------------------------------------------------------------------------------------
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
        # Delete the created component during the test
        deleteComponent(self.createdComponentID)

class ReadComponentTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create a component to be read in the tests and save its ID as its needed later for the teardown.
        self.createdComponentID = createComponent(ReadComponentTestsIO.fixture["component"])["ID"]

    def testReadComponent(self):
        # Attempt to read all components
        result = readComponent(self.createdComponentID)
        # Check the return type of the operation
        self.assertEqual(type(result),
                         ReadComponentTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as required by the specification")
        # Check whether the required information by the specification is returned
        self.assertTrue(all(key in result for key in ReadComponentTestsIO.outputs["returnedDictKeys"]),
                        "The information required by the specification was not returned")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created component during the tests
        deleteComponent(self.createdComponentID)

class ReadComponentsTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create components to be read in the tests and save their IDs as they are needed later for the teardown.
        self.createdComponentsIDs = []
        for component in ReadComponentsTestsIO.fixture["components"]:
            self.createdComponentsIDs.append(createComponent(component)["ID"])

    def testReadComponents(self):
        # Attempt to read all components
        result = readComponents()
        # Check the return type of the operation
        self.assertEqual(type(result),
                         ReadComponentsTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as required by the specification")
        # Check the type of the child objects as the return type is a container
        self.assertEqual(type(next(iter(result))),
                         ReadComponentsTestsIO.outputs["returnedChildType"],
                         "The return value child doesn't have the correct type, as required by the specification")
        # Check whether the required information by the specification is returned
        for component in result:
            self.assertTrue(all(key in component for key in ReadComponentsTestsIO.outputs["returnedDictKeys"]),
                            "The information required by the specification was not returned")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete all created components during the tests
        for ID in self.createdComponentsIDs:
            deleteComponent(ID)

class UpdateComponentTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create a component to test if it can be updated
        self.createdComponentID = createComponent(UpdateComponentTestsIO.fixture["component"])["ID"]

    def testUpdateComponent(self):
        # Attempt to update the component with a new status
        updateComponent(self.createdComponentID, UpdateComponentTestsIO.inputs["status"])

        # Check wether the operation altred the state of the status site
        self.assertEqual(readComponent(self.createdComponentID)["status"],
                         UpdateComponentTestsIO.outputs["status"],
                         "The component was not updated at the status site after attempting to update it")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created component during the test
        deleteComponent(self.createdComponentID)

class DeleteComponentTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create a component to test if it can be deleted
        self.createdComponentID = createComponent(DeleteComponentTestsIO.fixture["component"])["ID"]

    def testDeleteComponent(self):
        # Attempt to delete the test component
        deleteComponent(self.createdComponentID)

    # Teardown after EVERY test method
    def tearDown(self):
        pass


# ----------------------------------------------------------------------------------------------------------------------
## Incidents API Tests:
class CreateIncidentTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        pass

    def testCreateIncident(self):
        # Attempt to create an incident
        result = createIncident(CreateIncidentTestsIO.inputs["incident"])
        # See if the creation actually altred the state of the status site
        self.assertIn(CreateIncidentTestsIO.inputs["incident"]["name"], 
                      map(lambda x: x["name"], readIncidents()), 
                      "The incident was not returend by the status site after attempted creation")
        # Check the return type of the operation
        self.assertEqual(type(result),
                         CreateIncidentTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as defined by the specification")
        # Check whether the required information by the specification is returned
        self.assertTrue(all(key in result for key in CreateIncidentTestsIO.outputs["returnedDictKeys"]),
                        "The information required by the specification was not returned")

        # Save the ID as it is needed later for the teardown
        self.createdIncidentID = result["ID"]

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created component during the test
        deleteIncident(self.createdIncidentID)

class CreateIncidentUpdateTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create an incident to test if it could be updated. Also save its ID as it is needed in the teardown
        self.createdIncidentID = createIncident(CreateIncidentUpdateTestsIO.fixture["incident"])["ID"]

    def testCreateIncidentUpdate(self):
        # Attempt to create an incident update to the test incident
        result = createIncidentUpdate(self.createdIncidentID, CreateIncidentUpdateTestsIO.inputs["incidentUpdate"])
        # See if the creation actually altred the state of the status site
        self.assertEqual(len(readIncidentUpdates(self.createdIncidentID)), 
                         1, 
                         "Exactly one incident update was created, but the number of returend updates doesn't match")
        # Check the return type of the operation
        self.assertEqual(type(result),
                         CreateIncidentUpdateTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as defined by the specification")
        # Check whether the required information by the specification is returned
        self.assertTrue(all(key in result for key in CreateIncidentUpdateTestsIO.outputs["returnedDictKeys"]),
                        "The information required by the specification was not returned")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created incident during the test, which automatically also deletes all its updates
        deleteIncident(self.createdIncidentID)

class ReadIncidentTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create an incident to be read in the tests and save its ID as its needed later for the teardown.
        self.createdIncidentID = createIncident(ReadIncidentTestsIO.fixture["incident"])["ID"]

    def testReadIncident(self):
        # Attempt to read the previously created incident
        result = readIncident(self.createdIncidentID)
        # Check the return type of the operation
        self.assertEqual(type(result),
                         ReadIncidentTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as required by the specification")
        # Check whether the required information by the specification is returned
        self.assertTrue(all(key in result for key in ReadIncidentTestsIO.outputs["returnedDictKeys"]),
                        "The information required by the specification was not returned")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created incident during the tests
        deleteIncident(self.createdIncidentID)

class ReadIncidentsTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create some incidents to be read in the tests and save their IDs as they are needed later for the teardown.
        self.createdIncidentsIDs = []
        for incident in ReadIncidentsTestsIO.fixture["incidents"]:
            self.createdIncidentsIDs.append(createIncident(incident)["ID"])

    def testReadIncidents(self):
        # Attempt to read all components
        result = readIncidents()
        # Check the return type of the operation
        self.assertEqual(type(result),
                         ReadIncidentsTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as required by the specification")
        # Check the type of the child objects as the return type is a container
        self.assertEqual(type(next(iter(result))),
                         ReadIncidentsTestsIO.outputs["returnedChildType"],
                         "The return value child doesn't have the correct type, as required by the specification")
        # Check whether the required information by the specification is returned
        for component in result:
            self.assertTrue(all(key in component for key in ReadIncidentsTestsIO.outputs["returnedDictKeys"]),
                            "The information required by the specification was not returned")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete all created incidents during the tests
        for ID in self.createdIncidentsIDs:
            deleteIncident(ID)

# class ReadIncidentUpdateTests(unittest.TestCase):
#     # Setup for EVERY test method
#     def setUp(self):
#         # Create an incident and save its ID then populate it with updates to be read in the tests.
#         self.createdIncidentID = createIncident(ReadIncidentUpdatesTestsIO.fixture["incident"])["ID"]
#         self.createdIncidentUpdatesIDs = []
#         for update in ReadIncidentUpdatesTestsIO.fixture["updates"]:
#             self.createdIncidentUpdatesIDs.append(createIncidentUpdate(self.createdIncidentID, update)["ID"])

#     def testReadIncidentUpdate(self):
#         # Attempt to read all incident updates
#         result = readIncidentUpdates(self.createdIncidentID)
#         # Check the return type of the operation
#         self.assertEqual(type(result),
#                             ReadIncidentUpdatesTestsIO.outputs["returnedType"],
#                             "The return value doesn't have the correct type, as required by the specification")
#         # Check the type of the child objects as the return type is a container
#         self.assertEqual(type(next(iter(result))),
#                             ReadIncidentUpdatesTestsIO.outputs["returnedChildType"],
#                             "The return value child doesn't have the correct type, as required by the specification")
#         # Check whether the required information by the specification is returned
#         for component in result:
#             self.assertTrue(all(key in component for key in ReadIncidentUpdatesTestsIO.outputs["returnedDictKeys"]),
#                             "The information required by the specification was not returned")

#     # Teardown after EVERY test method
#     def tearDown(self):
#         # Delete the created incident during the test, which automatically also deletes all its updates
#         deleteIncident(self.createdIncidentID)

class ReadIncidentUpdatesTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create an incident and save its ID then populate it with updates to be read in the tests.
        self.createdIncidentID = createIncident(ReadIncidentUpdatesTestsIO.fixture["incident"])["ID"]
        self.createdIncidentUpdatesIDs = []
        for update in ReadIncidentUpdatesTestsIO.fixture["updates"]:
            self.createdIncidentUpdatesIDs.append(createIncidentUpdate(self.createdIncidentID, update)["ID"])

    def testReadIncidentUpdates(self):
        # Attempt to read all incident updates
        result = readIncidentUpdates(self.createdIncidentID)
        # Check the return type of the operation
        self.assertEqual(type(result),
                         ReadIncidentUpdatesTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as required by the specification")
        # Check the type of the child objects as the return type is a container
        self.assertEqual(type(next(iter(result))),
                         ReadIncidentUpdatesTestsIO.outputs["returnedChildType"],
                         "The return value child doesn't have the correct type, as required by the specification")
        # Check whether the required information by the specification is returned
        for component in result:
            self.assertTrue(all(key in component for key in ReadIncidentUpdatesTestsIO.outputs["returnedDictKeys"]),
                            "The information required by the specification was not returned")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created incident during the test, which automatically also deletes all its updates
        deleteIncident(self.createdIncidentID)

class ReadIncidentUpdatesTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create an incident and save its ID then populate it with updates to be read in the tests.
        self.createdIncidentID = createIncident(ReadIncidentUpdatesTestsIO.fixture["incident"])["ID"]
        self.createdIncidentUpdatesIDs = []
        for update in ReadIncidentUpdatesTestsIO.fixture["updates"]:
            self.createdIncidentUpdatesIDs.append(createIncidentUpdate(self.createdIncidentID, update)["ID"])

    def testReadIncidentUpdates(self):
        # Attempt to read all incident updates
        result = readIncidentUpdates(self.createdIncidentID)
        # Check the return type of the operation
        self.assertEqual(type(result),
                         ReadIncidentUpdatesTestsIO.outputs["returnedType"],
                         "The return value doesn't have the correct type, as required by the specification")
        # Check the type of the child objects as the return type is a container
        self.assertEqual(type(next(iter(result))),
                         ReadIncidentUpdatesTestsIO.outputs["returnedChildType"],
                         "The return value child doesn't have the correct type, as required by the specification")
        # Check whether the required information by the specification is returned
        for component in result:
            self.assertTrue(all(key in component for key in ReadIncidentUpdatesTestsIO.outputs["returnedDictKeys"]),
                            "The information required by the specification was not returned")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created incident during the test, which automatically also deletes all its updates
        deleteIncident(self.createdIncidentID)

class UpdateIncidentTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create an incident to test if it can be updated
        self.createdIncidentID = createIncident(UpdateIncidentTestsIO.fixture["incident"])["ID"]

    def testUpdateIncident(self):
        # Attempt to update the incident with a new body
        updateIncident(self.createdIncidentID, UpdateIncidentTestsIO.inputs["incidentBody"])

        # Check wether the operation altred the state of the status site
        self.assertEqual(readIncident(self.createdIncidentID)["body"],
                         UpdateIncidentTestsIO.outputs["incidentBody"],
                         "The incident was not updated at the status site after attempting to update it")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created incident during the test
        deleteIncident(self.createdIncidentID)

class UpdateIncidentUpdateTests(unittest.TestCase):
    # Setup for EVERY test method
    def setUp(self):
        # Create an incident and an incident update to test if it can be updated
        self.createdIncidentID = createIncident(UpdateIncidentUpdateTestsIO.fixture["incident"])["ID"]
        self.createdIncidentUpdateID = createIncidentUpdate(self.createdIncidentID, 
                                                            UpdateIncidentUpdateTestsIO.fixture["update"])['ID']
        # Also update `UpdateIncidentUpdateTestsIO.inputs["update"]` with the incident update ID as this
        # is needed by the call to `updateIncidentUpdate` below
        UpdateIncidentUpdateTestsIO.inputs["update"]['ID'] = self.createdIncidentUpdateID

    def testUpdateIncidentUpdate(self):
        # Attempt to update the incident update with a new status
        updateIncidentUpdate(self.createdIncidentID, UpdateIncidentUpdateTestsIO.inputs["update"])

        # Check wether the operation altred the state of the status site
        self.assertEqual(readIncidentUpdate(self.createdIncidentID, self.createdIncidentUpdateID)["formatedBody"],
                         UpdateIncidentUpdateTestsIO.outputs["formatedBody"],
                         "The incident update was not updated at the status site after attempting to update it")

    # Teardown after EVERY test method
    def tearDown(self):
        # Delete the created incident during the test
        deleteIncident(self.createdIncidentID)

# class DeleteIncidentTests(unittest.TestCase):
#     # Setup for EVERY test method
#     def setUp(self):
#         # Create a component to test if it can be deleted
#         self.createdComponentID = createComponent(DeleteComponentTestsIO.fixture["component"])["ID"]

#     def testDeleteIncident(self):
#         # Attempt to delete the test component
#         deleteComponent(self.createdComponentID)

#     # Teardown after EVERY test method
#     def tearDown(self):
#         pass

# class DeleteIncidentUpdateTests(unittest.TestCase):
#     # Setup for EVERY test method
#     def setUp(self):
#         # Create a component to test if it can be deleted
#         self.createdComponentID = createComponent(DeleteComponentTestsIO.fixture["component"])["ID"]

#     def testDeleteIncidentUpdate(self):
#         # Attempt to delete the test component
#         deleteComponent(self.createdComponentID)

#     # Teardown after EVERY test method
#     def tearDown(self):
#         pass


if __name__ == "__main__":
    # Configuring the executed tests
    ## Here you can turn off individual tests
    GroupsAPITests = unittest.TestSuite()
    GroupsAPITests.addTest(CreateGroupTests("testCreateGroup"))
    GroupsAPITests.addTest(ReadGroupTests("testReadGroup"))
    GroupsAPITests.addTest(ReadGroupsTests("testReadGroups"))
    GroupsAPITests.addTest(DeleteGroupsTests("testDeleteGroup"))

    ComponentsAPITests = unittest.TestSuite()
    ComponentsAPITests.addTest(CreateComponentTests("testCreateComponent"))
    ComponentsAPITests.addTest(ReadComponentTests("testReadComponent"))
    ComponentsAPITests.addTest(ReadComponentsTests("testReadComponents"))
    ComponentsAPITests.addTest(UpdateComponentTests("testUpdateComponent"))
    ComponentsAPITests.addTest(DeleteComponentTests("testDeleteComponent"))

    IncidentsAPITests = unittest.TestSuite()
    IncidentsAPITests.addTest(CreateIncidentTests("testCreateIncident"))
    IncidentsAPITests.addTest(CreateIncidentUpdateTests("testCreateIncidentUpdate"))
    IncidentsAPITests.addTest(ReadIncidentTests("testReadIncident"))
    IncidentsAPITests.addTest(ReadIncidentsTests("testReadIncidents"))
    # IncidentsAPITests.addTest(ReadIncidentUpdatesTests("testReadIncidentUpdate"))
    IncidentsAPITests.addTest(ReadIncidentUpdatesTests("testReadIncidentUpdates"))
    IncidentsAPITests.addTest(UpdateIncidentTests("testUpdateIncident"))
    IncidentsAPITests.addTest(UpdateIncidentUpdateTests("testUpdateIncidentUpdate"))
    # IncidentsAPITests.addTest(DeleteIncidentTests("testDeleteIncident"))
    # IncidentsAPITests.addTest(DeleteIncidentUpdateTests("testDeleteIncidentUpdate"))

    ## Here you can turn off whole suites
    APITest = unittest.TestSuite()
    APITest.addTest(GroupsAPITests)
    APITest.addTest(ComponentsAPITests)
    APITest.addTest(IncidentsAPITests)

    # Running the tests
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(APITest)


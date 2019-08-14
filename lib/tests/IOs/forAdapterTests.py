from lib.internals.structures.enums import ComponentStatus
from lib.internals.structures.enums import IncidentStatus
from lib.internals.structures.enums import IncidentUpdateAction


# Groups API Tests -----------------------------------------------------------------------------------------------------
class CreateGroupTestsIO:
    fixture = {

    }

    inputs = {
        "name": "test_create"
    }

    outputs = {
        "returnedType": dict,
        "returnedDictKeys": ["ID"]
    }

class ReadGroupTestsIO:
    fixture = {
        "name": "test_read"
    }

    inputs = {

    }

    outputs = {
        "returnedType": dict,
        "returnedDictKeys": ["name", "ID"]
    }

class ReadGroupsTestsIO:
    fixture = {
        "names": ["test_read1", "test_read2", "test_read3"]
    }

    inputs = {

    }

    outputs = {
        "returnedType": list,
        "returnedChildType": ReadGroupTestsIO.outputs["returnedType"],
        "returnedDictKeys": ReadGroupTestsIO.outputs["returnedDictKeys"]
    }

class DeleteGroupTestsIO:
    fixture = {
        "name": "test_delete"
    }

    inputs = {

    }

    outputs = {

    }


# Components API Tests -------------------------------------------------------------------------------------------------
class CreateComponentTestsIO:
    fixture = {

    }

    inputs = {
        "component": {
            'ID': None,
            'groupName': None,
            'groupID': None,
            'verbalStatus': "operational",
            'name': "test_create",
            'description': "test test test test",
            'status': ComponentStatus.Operational,
            'provider': "test"
        }
    }

    outputs = {
        "returnedType": dict,
        "returnedDictKeys": ["ID"]
    }

class ReadComponentTestsIO:
    fixture = {
        "component": {
            'ID': None,
            'groupName': None,
            'groupID': None,
            'verbalStatus': "operational",
            'name': "test_update",
            'description': "test test test test",
            'status': ComponentStatus.Operational,
            'provider': "test"
        }
    }

    inputs = {

    }

    outputs = {
        "returnedType": dict,
        "returnedDictKeys": ["name", "ID", "status", "groupID"]
    }

class ReadComponentsTestsIO:
    fixture = {
        "components": [
            {'ID': None,
             'groupName': None,
             'groupID': None,
             'verbalStatus': "operational",
             'name': "test_read1",
             'description': "test test test test",
             'status': ComponentStatus.Operational,
             'provider': "test"},
            {'ID': None,
            'groupName': None,
            'groupID': None,
            'verbalStatus': "operational",
            'name': "test_read2",
            'description': "test test test test",
            'status': ComponentStatus.Operational,
            'provider': "test"},
            {'ID': None,
            'groupName': None,
            'groupID': None,
            'verbalStatus': "operational",
            'name': "test_read3",
            'description': "test test test test",
            'status': ComponentStatus.Operational,
            'provider': "test"}
        ]
    }

    inputs = {

    }

    outputs = {
        "returnedType": list,
        "returnedChildType": ReadComponentTestsIO.outputs["returnedType"],
        "returnedDictKeys": ReadComponentTestsIO.outputs["returnedDictKeys"]
    }

class UpdateComponentTestsIO:
    fixture = {
        "component": {
            'ID': None,
            'groupName': None,
            'groupID': None,
            'verbalStatus': "operational",
            'name': "test_update",
            'description': "test test test test",
            'status': ComponentStatus.Operational,
            'provider': "test"
        }
    }

    inputs = {
        "status": ComponentStatus.PerformanceIssues
    }

    outputs = {
        "status": inputs["status"]
    }

class DeleteComponentTestsIO:
    fixture = {
        "component": {
            'ID': None,
            'groupName': None,
            'groupID': None,
            'verbalStatus': "operational",
            'name': "test_delete",
            'description': "test test test test",
            'status': ComponentStatus.Operational,
            'provider': "test"
        }
    }

    inputs = {

    }

    outputs = {

    }


# Incidents API Tests --------------------------------------------------------------------------------------------------
class CreateIncidentTestsIO:
    fixture = {

    }

    inputs = {
        "incident": {
            "title": "test_create",
            "ID": None,
            "status": IncidentStatus.Investigating,
            "verbalStatus": "Investigating",
            "body": "test test",
            "componentNames": None,
            "componenIDs": None,
            "componentStatuses": None,
            "componentVerbalStatuses": None,
            "updates": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "creationDate": None, # The same comment as for the "updates" key.
            "lastUpdateDate": None, # The same comment as for the "updates" key.
            "link": None, # The same comment as for the "updates" key.
            "provider": None, # The same comment as for the "updates" key.
            "language": None # The same comment as for the "updates" key.
        }
    }

    outputs = {
        "returnedType": dict,
        "returnedDictKeys": ["ID"]
    }

class CreateIncidentUpdateTestsIO:
    fixture = {
        "incident": {
            "title": "test_create_update",
            "ID": None,
            "status": IncidentStatus.Investigating,
            "verbalStatus": "Investigating",
            "body": "test test",
            "componentNames": None,
            "componenIDs": None,
            "componentStatuses": None,
            "componentVerbalStatuses": None,
            "updates": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "creationDate": None, # The same comment as for the "updates" key.
            "lastUpdateDate": None, # The same comment as for the "updates" key.
            "link": None, # The same comment as for the "updates" key.
            "provider": None, # The same comment as for the "updates" key.
            "language": None # The same comment as for the "updates" key.
        }
    }

    inputs = {
        "incidentUpdate": {
            "action": IncidentUpdateAction.Investigating,
            "ID": None,
            "date": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "incidentID": None, # The same comment as for the "date" key.
            "incidentStatus": IncidentStatus.Investigating,
            "rawBody": None, # The same comment as for the "date" key.
            "formatedBody": "Test test test"
        }
    }

    outputs = {
        "returnedType": dict,
        "returnedDictKeys": ["ID"]
    }

class ReadIncidentTestsIO:
    fixture = {
        "incident": {
            "title": "test_read",
            "ID": None,
            "status": IncidentStatus.Investigating,
            "verbalStatus": "Investigating",
            "body": "test test",
            "componentNames": None,
            "componenIDs": None,
            "componentStatuses": None,
            "componentVerbalStatuses": None,
            "updates": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "creationDate": None, # The same comment as for the "updates" key.
            "lastUpdateDate": None, # The same comment as for the "updates" key.
            "link": None, # The same comment as for the "updates" key.
            "provider": None, # The same comment as for the "updates" key.
            "language": None # The same comment as for the "updates" key.
        }
    }

    inputs = {

    }

    outputs = {
        "returnedType": dict,
        "returnedDictKeys": ["title", "ID", "status", "body"]
    }

class ReadIncidentsTestsIO:
    fixture = {
        "incidents": [
            {
                "title": "test_read1",
                "ID": None,
                "status": IncidentStatus.Investigating,
                "verbalStatus": "Investigating",
                "body": "test test",
                "componentNames": None,
                "componenIDs": None,
                "componentStatuses": None,
                "componentVerbalStatuses": None,
                "updates": None, # Normally not allowable when passed to the function but is okay for testing purposes.
                "creationDate": None, # The same comment as for the "updates" key.
                "lastUpdateDate": None, # The same comment as for the "updates" key.
                "link": None, # The same comment as for the "updates" key.
                "provider": None, # The same comment as for the "updates" key.
                "language": None # The same comment as for the "updates" key.
            },
            {   
                "title": "test_read2",
                "ID": None,
                "status": IncidentStatus.Fixed,
                "verbalStatus": "Fixed",
                "body": "test test",
                "componentNames": None,
                "componenIDs": None,
                "componentStatuses": None,
                "componentVerbalStatuses": None,
                "updates": None, # Normally not allowable when passed to the function but is okay for testing purposes.
                "creationDate": None, # The same comment as for the "updates" key.
                "lastUpdateDate": None, # The same comment as for the "updates" key.
                "link": None, # The same comment as for the "updates" key.
                "provider": None, # The same comment as for the "updates" key.
                "language": None # The same comment as for the "updates" key.
            },
            {
                "title": "test_read3",
                "ID": None,
                "status": IncidentStatus.Investigating,
                "verbalStatus": "Investigating",
                "body": "test test",
                "componentNames": None,
                "componenIDs": None,
                "componentStatuses": None,
                "componentVerbalStatuses": None,
                "updates": None, # Normally not allowable when passed to the function but is okay for testing purposes.
                "creationDate": None, # The same comment as for the "updates" key.
                "lastUpdateDate": None, # The same comment as for the "updates" key.
                "link": None, # The same comment as for the "updates" key.
                "provider": None, # The same comment as for the "updates" key.
                "language": None # The same comment as for the "updates" key.
            }
        ]
    }

    inputs = {

    }

    outputs = {
        "returnedType": list,
        "returnedChildType": ReadIncidentTestsIO.outputs["returnedType"],
        "returnedDictKeys": ReadIncidentTestsIO.outputs["returnedDictKeys"]
    }

class ReadIncidentUpdateTestsIO:
    fixture = {
        "incident": {
            "title": "test_read",
            "ID": None,
            "status": IncidentStatus.Investigating,
            "verbalStatus": "Investigating",
            "body": "test test",
            "componentNames": None,
            "componenIDs": None,
            "componentStatuses": None,
            "componentVerbalStatuses": None,
            "updates": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "creationDate": None, # The same comment as for the "updates" key.
            "lastUpdateDate": None, # The same comment as for the "updates" key.
            "link": None, # The same comment as for the "updates" key.
            "provider": None, # The same comment as for the "updates" key.
            "language": None # The same comment as for the "updates" key.
        },
        "update":{
            "action": IncidentUpdateAction.Investigating,
            "ID": None,
            "date": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "incidentID": None, # The same comment as for the "date" key.
            "incidentStatus": IncidentStatus.Investigating,
            "rawBody": None, # The same comment as for the "date" key.
            "formatedBody": "Test1 test1 test1"
        }
    }

    inputs = {

    }

    outputs = {
        "returnedType": dict,
        "returnedDictKeys": ["ID", "incidentStatus", "formatedBody"]
    }

class ReadIncidentUpdatesTestsIO:
    fixture = {
        "incident": {
            "title": "test_read",
            "ID": None,
            "status": IncidentStatus.Investigating,
            "verbalStatus": "Investigating",
            "body": "test test",
            "componentNames": None,
            "componenIDs": None,
            "componentStatuses": None,
            "componentVerbalStatuses": None,
            "updates": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "creationDate": None, # The same comment as for the "updates" key.
            "lastUpdateDate": None, # The same comment as for the "updates" key.
            "link": None, # The same comment as for the "updates" key.
            "provider": None, # The same comment as for the "updates" key.
            "language": None # The same comment as for the "updates" key.
        },
        "updates": [
            {
                "action": IncidentUpdateAction.Investigating,
                "ID": None,
                "date": None, # Normally not allowable when passed to the function but is okay for testing purposes.
                "incidentID": None, # The same comment as for the "date" key.
                "incidentStatus": IncidentStatus.Investigating,
                "rawBody": None, # The same comment as for the "date" key.
                "formatedBody": "Test1 test1 test1"
            },
            {
                "action": IncidentUpdateAction.Identified,
                "ID": None,
                "date": None, # Normally not allowable when passed to the function but is okay for testing purposes.
                "incidentID": None, # The same comment as for the "date" key.
                "incidentStatus": IncidentStatus.Identified,
                "rawBody": None, # The same comment as for the "date" key.
                "formatedBody": "Test2 test2 test2"
            },
            {
                "action": IncidentUpdateAction.Update,
                "ID": None,
                "date": None, # Normally not allowable when passed to the function but is okay for testing purposes.
                "incidentID": None, # The same comment as for the "date" key.
                "incidentStatus": IncidentStatus.Identified,
                "rawBody": None, # The same comment as for the "date" key.
                "formatedBody": "Test3 test3 test3"
            }
        ]
    }

    inputs = {

    }

    outputs = {
        "returnedType": list,
        "returnedChildType": ReadIncidentUpdateTestsIO.outputs["returnedType"],
        "returnedDictKeys": ReadIncidentUpdateTestsIO.outputs["returnedDictKeys"]
    }

class UpdateIncidentTestsIO:
    fixture = {
        "incident": {
            "title": "test_update",
            "ID": None,
            "status": IncidentStatus.Investigating,
            "verbalStatus": "Investigating",
            "body": "test test",
            "componentNames": None,
            "componenIDs": None,
            "componentStatuses": None,
            "componentVerbalStatuses": None,
            "updates": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "creationDate": None, # The same comment as for the "updates" key.
            "lastUpdateDate": None, # The same comment as for the "updates" key.
            "link": None, # The same comment as for the "updates" key.
            "provider": None, # The same comment as for the "updates" key.
            "language": None # The same comment as for the "updates" key.
        }
    }

    inputs = {
        "incidentBody": "updated updated"
    }

    outputs = {
        "incidentBody": inputs["incidentBody"]
    }

class UpdateIncidentUpdateTestsIO:
    fixture = {
        "incident": {
            "title": "test_update_update",
            "ID": None,
            "status": IncidentStatus.Investigating,
            "verbalStatus": "Investigating",
            "body": "test test",
            "componentNames": None,
            "componenIDs": None,
            "componentStatuses": None,
            "componentVerbalStatuses": None,
            "updates": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "creationDate": None, # The same comment as for the "updates" key.
            "lastUpdateDate": None, # The same comment as for the "updates" key.
            "link": None, # The same comment as for the "updates" key.
            "provider": None, # The same comment as for the "updates" key.
            "language": None # The same comment as for the "updates" key.
        },
        "update": {
            "action": IncidentUpdateAction.Investigating,
            "ID": None,
            "date": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "incidentID": None, # The same comment as for the "date" key.
            "incidentStatus": IncidentStatus.Investigating,
            "rawBody": None, # The same comment as for the "date" key.
            "formatedBody": "Test test test"
        }
    }

    inputs = {
        "update": {
            "action": IncidentUpdateAction.Investigating,
            "ID": None,
            "date": None, # Normally not allowable when passed to the function but is okay for testing purposes.
            "incidentID": None, # The same comment as for the "date" key.
            "incidentStatus": IncidentStatus.Investigating,
            "rawBody": None, # The same comment as for the "date" key.
            "formatedBody": "Update Update Update"
        }
    }

    outputs = {
        "formatedBody": inputs['update']['formatedBody']
    }

class DeleteIncidentTestsIO:
    fixture = {

    }

    inputs = {

    }

    outputs = {

    }

class DeleteIncidentUpdateTestsIO:
    fixture = {

    }

    inputs = {

    }

    outputs = {

    }

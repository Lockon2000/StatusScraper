from lib.internals.structures.enums import ComponentStatus


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

class ReadGroupsTestsIO:
    fixture = {
        "names": ["test_read1", "test_read2", "test_read3"]
    }

    inputs = {

    }

    outputs = {
        "returnedType": list,
        "returnedChildType": CreateGroupTestsIO.outputs["returnedType"],
        "returnedDictKeys": ["ID", "name"]
    }

class DeleteGroupTestsIO:
    fixture = {
        "name": "test_delete"
    }

    inputs = {

    }

    outputs = {

    }

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
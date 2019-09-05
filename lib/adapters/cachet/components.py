import json

import requests

from lib.internals.utilities.configurationsInterface import APIBaseURL
from lib.internals.utilities.configurationsInterface import APIKey
from lib.internals.structures.enums import ComponentStatus


# Global options
objectsPerPage = 100000


# This function creates a component at cachet
def createComponent(component):
    # Input:
    #   component: A dict with necessary information to create the component. For a Refrence of 
    #              all contained information see the docs for components under crud.
    # Output:
    #   succeeded: Will return a dict with the response data required about the created component. The required
    #              information is specified in the docs at components under adapters.
    #   failed: Will raise a requests.HTTPError exception.

    payload = {
        'name': component['name'],
        'description': component['description'],
        # component['status'] is an enum, so it must be converted to the appropriate status code specific to cachet.
        'status': convertComponentEnumStatus(component['status']),
        'group_id': component['groupID'],
        # Whether the component is enabled or disabled.
        'enabled': 1
    }

    # Make an authenticated post request to the appropriate end point to create the component
    response = requests.post("{APIBaseURL}/components".format(APIBaseURL=APIBaseURL),
                             data=json.dumps(payload),
                             headers={
                                 'X-Cachet-Token': APIKey,
                                 'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # Create a dict representing the created component with the required information
    data = response.json()['data']
    result = {'ID': data['id']}

    return result

# This function reads a specific component at cachet given its ID and returns a dict with the needed information.
def readComponent(componentID):
    # Input:
    #   componentID: The ID of the component requested.
    # Output:
    #   succeeded: Will return a dict representing the requested component with the required information.
    #              The required information is specified in the docs at components under adapters.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated get request to the appropriate end point to read the component
    response = requests.get("{APIBaseURL}/components/{componentID}".format(APIBaseURL=APIBaseURL,
                                                                           componentID=componentID),
                            headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # Create the dict containing all required information about the component
    data = response.json()['data']
    result = {
            'name': data['name'],
            'ID': data['id'],
            'status': convertComponentPlainStatus(data['status']),
            'groupID': data['group_id']
    }

    return result

# This function reads all the components at cachet and returns a list with the needed information.
def readComponents(form="group: {component: ID}", caseSensitivity=True):
    # Input:
    #   None.
    # Output:
    #   succeeded: Will return a list of dicts where each dict represents a component and contains the
    #              rquired information about it.
    #              The required information is specified in the docs at components under adapters.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated get request to the appropriate end point to read all components
    response = requests.get("{APIBaseURL}/components".format(APIBaseURL=APIBaseURL),
                            params={"per_page": objectsPerPage},
                            headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # Create the list containing the dicts representing the retrieved components with the requiered information
    data = response.json()['data']
    result = [
        {
            'name': component['name'],
            'ID': component['id'],
            'status': convertComponentPlainStatus(component['status']),
            'groupID': component['group_id']
        }
        for component in data
    ]

    return result

# This function updates an existing component with a new status given its ID.
def updateComponent(componentID, componentStatus):
    # Input:
    #   componentID: An int specifying the ID of the component to be updated.
    #   componentStatus: An Enum value of class ComponentStatus.
    # Output:
    #   succeeded: Will return `None`.
    #   failed: Will raise a requests.HTTPError exception.

    payload = {
        'status': convertComponentEnumStatus(componentStatus)
    }


    # Make an authenticated get request to the appropriate end point to update the component
    response = requests.put("{APIBaseURL}/components/{componentID}".format(APIBaseURL=APIBaseURL,
                                                                           componentID=componentID),
                            data = json.dumps(payload),
                            headers = {
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

# This function deletes a component from cachet given its ID.
def deleteComponent(componentID):
    # Input:
    #   componentID: An int specifying the ID of the component to be deleted.
    # Output:
    #   succeeded: Will return `None`.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated delete request to the appropriate end point to delete the component
    response = requests.delete("{APIBaseURL}/components/{componentID}".format(APIBaseURL=APIBaseURL,
                                                                              componentID=componentID),
                               headers={'X-Cachet-Token': APIKey})
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()


# Helper functions -----------------------------------------------------------------------------------------------------
# This function is needed to convert the generalised component statuses as they are implemented
# as general enums to the cachet specific status codes for a component.
def convertComponentEnumStatus(componentEnumStatus):
    # Input:
    #   componentEnumStatus: An Enum value of class ComponentStatus.
    # Output:
    #   succeeded: The corresponding cachet status code for the ComponentStatus enum value.
    #   failed: Will return `None`

    if   componentEnumStatus == ComponentStatus.Operational:
        return 1
    elif componentEnumStatus == ComponentStatus.PerformanceIssues:
        return 2
    elif componentEnumStatus == ComponentStatus.PartialOutage:
        return 3
    elif componentEnumStatus == ComponentStatus.MajorOutage:
        return 4

# The inverse of `convertComponentEnumStatus`
def convertComponentPlainStatus(componentPlainStatus):
    # Input:
    #   componentPlainStatus: A cachet component status code.
    # Output:
    #   succeeded: The corresponding cachet status code for the ComponentStatus enum value.
    #   failed: Will return `None`

    if   componentPlainStatus == 1:
        return ComponentStatus.Operational
    elif componentPlainStatus == 2:
        return ComponentStatus.PerformanceIssues
    elif componentPlainStatus == 3:
        return ComponentStatus.PartialOutage
    elif componentPlainStatus == 4:
        return ComponentStatus.MajorOutage


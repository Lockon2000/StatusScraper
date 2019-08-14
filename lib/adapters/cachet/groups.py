import json
import requests

from conf.configs import API
from conf.configs import APIKey


# Global options
objectsPerPage = 100000

# This function creates a group at cachet
def createGroup(groupName):
    # Input:
    #   groupName: A string with the name of the group to be created.
    # Output:
    #   succeeded: Will return a dict with the response data containing required information about the created gourp.
    #              The required information is specified in the docs at groups under adapters.
    #   failed: Will raise a requests.HTTPError exception.

    payload = {
        'name': groupName,
        # Whether the group is publicly visible or not.
        # NOTE: this key value pair is not documented in the API docs. It should therefore be
        # tested if it has any effect or not at the nearest opportunity.
        'visible': 1,
        # Different options for 'collapsed':
        # 0: never collapsed
        # 1: always collapsed
        # 2: collapsed as long as there are no problems
        'collapsed': 1
    }

    # Make an authenticated post request to the appropriate end point to create the group
    response = requests.post("{API}/components/groups".format(API=API),
                             data=json.dumps(payload),
                             headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # Create a dict representing the created group with the required information
    data = response.json()['data']
    result = {'ID': data['id']}

    return result

# This function reads a specific group at cachet given its ID and returns a dict with the needed information.
def readGroup(groupID):
    # Input:
    #   groupID: The ID of the group requested.
    # Output:
    #   succeeded: Will return a dict representing the requested group with the required information.
    #              The required information is specified in the docs at groups under adapters.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated get request to the appropriate end point to read the group
    response = requests.get("{API}/components/groups/{groupID}".format(API=API, groupID=groupID),
                            headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # Create the dict containing all required information about the group
    data = response.json()['data']
    result = {
            'name': data['name'],
            'ID': data['id']
    }

    return result

# This function reads all the groups at cachet and returns a list with the needed information.
def readGroups():
    # Input:
    #   None.
    # Output:
    #   succeeded: Will return a list of dicts where each dict represents a group and contains the
    #              rquired information about it.
    #              The required information is specified in the docs at groups under adapters.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated get request to the appropriate end point to read all groups
    response = requests.get("{API}/components/groups".format(API=API),
                            params={"per_page": objectsPerPage},
                            headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # Create the list containing the dicts representing the retrieved groups with the requiered information
    data = response.json()['data']
    result = [
        {
            'name': group['name'],
            'ID': group['id']
        }
        for group in data
    ]

    return result

# This function deletes a group from cachet given its ID number.
def deleteGroup(groupID):
    # Input:
    #   groupID: An int specifying the ID of the group to be deleted.
    # Output:
    #   succeeded: Will return None.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated delete request to the appropriate end point to delete the group
    response = requests.delete("{API}/components/groups/{ID}".format(API=API, ID=groupID),
                               headers={'X-Cachet-Token': APIKey})
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()


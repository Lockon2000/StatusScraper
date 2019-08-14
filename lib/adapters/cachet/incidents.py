import json

import requests

from conf.configs import API
from conf.configs import APIKey
from lib.internals.structures.enums import IncidentStatus


# Global options
objectsPerPage = 100000


# This functions creates an incident at the status site with no updates, just the main body of the
# incident is created.
def createIncident(incident):
    # Input:
    #   incident: A dict with all necessary information to create the incident. For a Refrence of 
    #             all contained information see the docs for incidents under crud.
    # Output:
    #   succeeded: Will return a dict with the response data required about the created incident. The required
    #              information is specified in the docs at incidents under adapters.
    #   failed: Will raise a requests.HTTPError exception.    

    payload = {
        'name': incident['title'],
        'message': incident['body'],
        'status': convertIncidentEnumStatus(incident['status']),
        # Whether the incident is publicly visible
        'visible': 1,
        # Whether the incident should be sticked
        'stickied': 1,
        # Notify all subscribed users
        'notify': 1
    }

    # Make an authenticated post request to the appropriate end point to create the component
    response = requests.post("{API}/incidents".format(API=API),
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

# This function updates an existing incident with a new update reporting new events. Also if the incident update being
# created has status `IncidentStatus.Fixed` then the parent incident is being unsticked.
def createIncidentUpdate(incidentID, incidentUpdate):
    # Input:
    #   incidentID: The ID of the incident we wish to update.
    #   incidentUpdate: A dict representing the update supplying all necessery information. For a refrence of the
    #           supplied information see incidents under crud.
    # Output:
    #   succeeded: Will return a dict with the response data required about the created incident update. The 
    #              required information is specified in the docs at incidents under adapters.
    #   failed: Will raise a requests.HTTPError exception.
    payload = {
        'status': convertIncidentEnumStatus(incidentUpdate['incidentStatus']),
        'message': incidentUpdate['formatedBody']
    }

    # Make an authenticated post request to the appropriate end point to update the incident
    response = requests.post("{API}/incidents/{incidentID}/updates".format(API=API, incidentID=incidentID),
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

    # If incident update had a status of `IncidentStatus.Fixed` then remove the sticky property of the parent incident
    if incidentUpdate['incidentStatus'] == IncidentStatus.Fixed:
            payload = {
                'stickied': 0
            }

            # Make an authenticated put request to the appropriate end point to update the incident
            response = requests.put("{API}/incidents/{incidentID}".format(API=API, incidentID=incidentID),
                                    data=json.dumps(payload),
                                    headers={
                                        'X-Cachet-Token': APIKey,
                                        'Content-Type': "application/json"
                                    })
            # Raise HTTPError for all unsuccessful status codes.
            response.raise_for_status()

    return result

# This function reads a specific incidents at cachet given its ID and returns a dict with the needed information.
def readIncident(incidentID):
    # Input:
    #   incidentID: The ID of the incident requested.
    # Output:
    #   succeeded: Will return a dict representing the requested incident with the required information.
    #              The required information is specified in the docs at incidents under adapters.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated get request to the appropriate end point to read the incident
    response = requests.get("{API}/incidents/{incidentID}".format(API=API, incidentID=incidentID),
                            headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # Create the dict containing all required information about the incident
    data = response.json()['data']
    result = {
            'title': data['name'],
            'ID': data['id'],
            'status': convertIncidentPlainStatus(data['status']),
            'body': data['message']
    }

    return result

# This function reads all the incidents at cachet and returns a list with the needed information.
def readIncidents():
    # Input:
    #   None.
    # Output:
    #   succeeded: Will return a list of dicts where each dict represents an incident and contains the
    #              rquired information about it.
    #              The required information is specified in the docs at incidents under adapters.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated get request to the appropriate end point to read all incidents
    response = requests.get("{API}/incidents".format(API=API),
                            params={"per_page": objectsPerPage},
                            headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # Create the list containing the dicts representing the retrieved incidents with the requiered information
    data = response.json()['data']
    result = [
        {
            'title': incident['name'],
            'ID': incident['id'],
            'status': convertIncidentPlainStatus(incident['status']),
            'body': incident['message']
        }
        for incident in data
    ]

    return result

# This function reads a specific update for a specific incident at cachet and returns the needed information.
def readIncidentUpdate(incidentID, incidentUpdateID):
    # Input:
    #   incidentID: The ID of the incident whose update is requested.
    #   incidentUpdateID: The ID of the requested incident update.
    # Output:
    #   succeeded: Will return a dict which represents an incident update and contains the rquired information about
    #              it. The required information is specified in the docs at incidents under adapters.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated get request to the appropriate end point to read the incident update
    response = requests.get("{API}/incidents/{incidentID}/updates/{incidentUpdateID}".format(
                                                                                    API=API,
                                                                                    incidentID=incidentID,
                                                                                    incidentUpdateID=incidentUpdateID
                                                                                ),
                            params={"per_page": objectsPerPage},
                            headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # Create the list containing the dicts representing the retrieved incident updates with the requiered information
    data = response.json()['data']
    result = {
            'ID': data['id'],
            'incidentStatus': convertIncidentPlainStatus(data['status']),
            'formatedBody': data['message']
    }

    return result

# This function reads all the updates for a specific incident at cachet and returns the needed information.
def readIncidentUpdates(incidentID):
    # Input:
    #   incidentID: The ID of the incident whose updates are requested.
    # Output:
    #   succeeded: Will return a list of dicts where each dict represents an incident update and contains the
    #              rquired information about it.
    #              The required information is specified in the docs at incidents under adapters.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated get request to the appropriate end point to read all incident updates
    response = requests.get("{API}/incidents/{incidentID}/updates".format(API=API, incidentID=incidentID),
                            params={"per_page": objectsPerPage},
                            headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # Create the list containing the dicts representing the retrieved incident updates with the requiered information
    data = response.json()['data']
    result = [
        {
            'ID': incidentUpdate['id'],
            'incidentStatus': convertIncidentPlainStatus(incidentUpdate['status']),
            'formatedBody': incidentUpdate['message']
        }
        for incidentUpdate in data
    ]

    return result

# This function updates an existing incident with a new body given its ID.
def updateIncident(incidentID, incidentBody):
    # Input:
    #   incidentID: An int specifying the ID of the incident to be updated.
    #   incidentBody: A string specifying the new body for the incident.
    # Output:
    #   succeeded: Will return None.
    #   failed: Will raise a requests.HTTPError exception.

    payload = {
        'message': incidentBody
    }

    # Make an authenticated put request to the appropriate end point to update the incident
    response = requests.put("{API}/incidents/{incidentID}".format(API=API, incidentID=incidentID),
                             data=json.dumps(payload),
                             headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

# This function updates an existing incident update with a new body and incident status given its and 
# the parent incident's ID. Also if the incident update is being set to status `IncidentStatus.Fixed` then the parent
# incident is being unsticked.
def updateIncidentUpdate(incidentID, incidentUpdate):
    # Input:
    #   incidentUpdate: A dict representing the incident update containing all necessary information.
    #                   For a refrence about the contained information see the docs for incidents under crud.
    #   incidentID: An int specifying the ID of the incident to which this update belongs.
    # Output:
    #   succeeded: Will return None.
    #   failed: Will raise a requests.HTTPError exception.

    payload = {
        'status': convertIncidentEnumStatus(incidentUpdate['incidentStatus']),
        'message': incidentUpdate['formatedBody']
    }

    # Make an authenticated put request to the appropriate end point to update the incident update
    response = requests.put("{API}/incidents/{incidentID}/updates/{incidentUpdateID}".format(
                                                                              API=API,
                                                                              incidentID=incidentID, 
                                                                              incidentUpdateID=incidentUpdate['ID']
                                                                            ),
                             data=json.dumps(payload),
                             headers={
                                'X-Cachet-Token': APIKey,
                                'Content-Type': "application/json"
                            })
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

    # If incident was updated to a status of `IncidentStatus.Fixed` then remove the sticky property of the incident
    if incidentUpdate['incidentStatus'] == IncidentStatus.Fixed:
            payload = {
                'stickied': 0
            }

            # Make an authenticated put request to the appropriate end point to update the incident
            response = requests.put("{API}/incidents/{incidentID}".format(API=API, incidentID=incidentID),
                                    data=json.dumps(payload),
                                    headers={
                                        'X-Cachet-Token': APIKey,
                                        'Content-Type': "application/json"
                                    })
            # Raise HTTPError for all unsuccessful status codes.
            response.raise_for_status()

# This function deletes an incident from cachet given its ID.
def deleteIncident(incidentID):
    # Input:
    #   incidentID: An int specifying the ID of the incident to be deleted.
    # Output:
    #   succeeded: Will return None.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated delete request to the appropriate end point to delete the incident
    response = requests.delete("{API}/incidents/{ID}".format(API=API, ID=incidentID),
                               headers={'X-Cachet-Token': APIKey})
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()

# This function deletes an incident update from cachet given its and the incidents ID.
def deleteIncidentUpdate(incidentUpdateID, incidentID):
    # Input:
    #   incidentUpdateID: An int specifying the ID of the incident update to be deleted.
    #   incidentID: An int specifying the ID of the incident to which this update belongs.
    # Output:
    #   succeeded: Will return None.
    #   failed: Will raise a requests.HTTPError exception.

    # Make an authenticated delete request to the appropriate end point to delete the incident update
    response = requests.delete("{API}/incidents/{incidentID}/updates/{incidentUpdateID}".format(
                                                                            API=API,
                                                                            incidentID=incidentID, 
                                                                            incidentUpdateID=incidentUpdateID
                                                                        ),
                               headers={'X-Cachet-Token': APIKey})
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()


# Helper functions -----------------------------------------------------------------------------------------------------
# This function is needed to convert the generalised incident statuses as they are implemented
# as a general enum to the cachet specific status codes for an incident.
def convertIncidentEnumStatus(incidentEnumStatus):
    # Input:
    #   incidentEnumStatus: An Enum value of class IncidentStatus.
    # Output:
    #   The corresponding cachet status code for the IncidentStatus enum value.
    if   incidentEnumStatus == IncidentStatus.Investigating:
        return 1
    elif incidentEnumStatus == IncidentStatus.Identified:
        return 2
    elif incidentEnumStatus == IncidentStatus.Watching:
        return 3
    elif incidentEnumStatus == IncidentStatus.Fixed:
        return 4

# The inverse of `convertIncidentEnumStatus`
def convertIncidentPlainStatus(incidentPlainStatus):
    # Input:
    #   incidentPlainStatus: A cachet incident status code.
    # Output:
    #   succeeded: The corresponding cachet status code for the IncidentStatus enum value.
    #   failed: Will return `None`

    if   incidentPlainStatus == 1:
        return IncidentStatus.Investigating
    elif incidentPlainStatus == 2:
        return IncidentStatus.Identified
    elif incidentPlainStatus == 3:
        return IncidentStatus.Watching
    elif incidentPlainStatus == 4:
        return IncidentStatus.Fixed


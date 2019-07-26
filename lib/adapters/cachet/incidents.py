import json

import requests

from conf.configs import API
from conf.configs import APIKey


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
        'name': incident['name']
        'message': incident['body']
        'status': convertIncidentStatusEnumValue(incident['status'])
        # Whether the incident is publicly visible
        'visible': 1
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

# This function updates an existing incident with a new update reporting new events
def createIncidentUpdate(incidentID, update):
    # Input:
    #   incidentID: The ID of the incident we wish to update.
    #   update: A dict representing the update supplying all necessery information. For a refrence of the
    #           supplied information see incidents under crud.
    # Output:
    #   succeeded: Will return None.
    #   failed: Will raise a requests.HTTPError exception.
    payload = {
        'status': convertIncidentStatusEnumValue(update['IncidentStatus'])
        'message': update['formatedBody']
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
            'name': incident['name'],
            'ID': incident['id'],
            'status': incident['status'],
            'body': incident['message']
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
            'name': incident['name'],
            'ID': incident['id'],
            'status': incident['status'],
            'body': incident['message']
        }
        for incident in data
    ]

    return result

# WIP ---------------------------------------- return value!!!!!

# This function reads all the updates for a specific incident at cachet and returns a list with the needed information.
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
# the incident ID.
def updateIncidentUpdate(incidentUpdate, incidentID)
    # Input:
    #   incidentUpdate: A dict representing the incident update containing all necessary information.
    #                   For a refrence about the contained information see the docs for incidents under crud.
    #   incidentID: An int specifying the ID of the incident to which this update belongs.
    # Output:
    #   succeeded: Will return None.
    #   failed: Will raise a requests.HTTPError exception.

    payload = {
        'status': convertIncidentStatusEnumValue(incidentUpdate['IncidentStatus']),
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
                                                                            incidentUpdateID=incidentUpdate['ID']
                                                                        ),
                               headers={'X-Cachet-Token': APIKey})
    # Raise HTTPError for all unsuccessful status codes.
    response.raise_for_status()


# Helper functions -----------------------------------------------------------------------------------------------------
# This function is needed to convert the generalised incident statuses as they are implemented
# as a general enum to the cachet specific status codes for an incident.
def convertIncidentStatusEnumValue(incidentStatusEnumValue):
    # Input:
    #   incidentStatusEnumValue: An Enum value of class IncidentStatus.
    # Output:
    #   The corresponding cachet status code for the IncidentStatus enum value.
    if   incidentStatusEnumValue == IncidentStatus.Investigating:
        return 1
    elif incidentStatusEnumValue == IncidentStatus.Identified:
        return 2
    elif incidentStatusEnumValue == IncidentStatus.Watching:
        return 3
    elif incidentStatusEnumValue == IncidentStatus.Fixed:
        return 4


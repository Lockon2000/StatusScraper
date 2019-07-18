import json

import requests

from conf.configs import API
from conf.configs import APIKey
from lib.internals.utilities.tools import log
from lib.internals.utilities.hashing import hashIncident


# Global options
objectsPerPage = 100000


# Helper functions
def createIncident(incident):
    payload = {}

    payload['name'] = incident['name']
    payload['message'] = incident['message']
    payload['status'] = incident['status']
    payload['component_id'] = incident['component_id']
    payload['component_status'] = incident['component_status']

    payload['visible'] = 1
    payload['notify'] = 1

    try:
        response = requests.post("{}/incidents".format(dtadCachetAPI),
                                 data=json.dumps(payload),
                                 headers={'X-Cachet-Token': APIKey,
                                          'Content-Type': "application/json"})
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Couldn't create incident {}".format(incident['name']))
        log("Error", "Unsuccessful HTTP POST Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    else:
        log("Success", "Created the incident \"{name}\" at the provider {providerName}".format(
                                                                                    name=incident['name'],
                                                                                    providerName=incident['provider']
                                                                                )
        )

        incidentID = response.json()['data']['id']
        numberOfNewUpdates = len(incident['updates'])
        updateIncident(incidentID, incident, numberOfNewUpdates)

def readIncidents(format="incidentHash: id"):
    result = {}
    
    try:
        response = requests.get("{dtadCachetAPI}/incidents?per_page={objectsPerPage}".format(
                                                                            dtadCachetAPI=dtadCachetAPI,
                                                                            objectsPerPage=objectsPerPage
                                                                        )
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Coulden't retrieve the Incidents from Cachet!!!")
        log("Error", "Unsuccessful HTTP Request! Error Code {}".format(str(e)))

    if format == "incidentHash: id":
        for incident in response.json()['data']:
            result[hashIncident(incident)] = incident['id']
    if format == "id: status":
        for incident in response.json()['data']:
            result[incident['id']] = incident['status']

    return result

def readIncidentUpdates(incidentID):
    try:
        response = requests.get("{dtadCachetAPI}/incidents/{incidentID}/updates".format(
                                                                dtadCachetAPI=dtadCachetAPI,
                                                                incidentID=incidentID
                                                            )
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Couldn't get the updates of the incident with the id {}".format(incidentID))
        log("Error", "Unsuccessful HTTP GET Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    
    return response.json()['data']

def updateIncident(incidentID, incident, numberOfNewUpdates):
    payload = {}

    payload['message'] = incident['message']

    try:
        response = requests.put("{dtadCachetAPI}/incidents/{incidentID}".format(
                                                                dtadCachetAPI=dtadCachetAPI,
                                                                incidentID=incidentID
                                                            ),
                                 data=json.dumps(payload),
                                 headers={'X-Cachet-Token': APIKey,
                                          'Content-Type': "application/json"})
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Couldn't update incident {}".format(incident['name']))
        log("Error", "Unsuccessful HTTP PUT Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    else:
        log("Success", "Updated the main body of incident \"{name}\" with the id {id}" \
            " at the provider {providerName}".format(
                                                name=incident['name'],
                                                id=incidentID,
                                                providerName=incident['provider']
                                            )
        )


    payload = {}

    latestUpdate = incident['updates'][-numberOfNewUpdates]
    payload['message'] = latestUpdate['message']
    payload['status'] = latestUpdate['status']

    try:
        response = requests.post("{dtadCachetAPI}/incidents/{incidentID}/updates".format(
                                                                dtadCachetAPI=dtadCachetAPI,
                                                                incidentID=incidentID
                                                            ),
                                 data=json.dumps(payload),
                                 headers={'X-Cachet-Token': APIKey,
                                          'Content-Type': "application/json"})
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Couldn't create an update for incident {}".format(incident['name']))
        log("Error", "Unsuccessful HTTP POST Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    else:
        log("Success", "Posted an updated for the incident \"{name}\" with the id {id}" \
            " at the provider {providerName}".format(
                                                name=incident['name'],
                                                id=incidentID,
                                                providerName=incident['provider']
                                            )
        )


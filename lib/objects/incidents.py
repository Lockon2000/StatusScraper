import json

import requests

from configs import dtadCachetAPI
from configs import APIKey
from enabledProviders import incidentFunctions
from lib.objects.components import updateComponentStatus
from lib.objects.components import latestComponentStatuses
from lib.utilities.cachet import getCachetComponents
from lib.utilities.cachet import getCachetIncident
from lib.utilities.hashing import hashIncident
from lib.utilities.tools import log


# Global options
debug = False


# Main functionality
def CRUDIncidents():
    incidentIDs = getCachetIncident("incidentHash: id")

    # Check which incidents and update them if already there or create them otherwise.
    for providerName, getIncidents in incidentFunctions:
        for incident in getIncidents():
            componentID = incident['component_id']
            componentStatus = incident['component_status']
            currentComponentStatus = latestComponentStatuses.get(componentID, 0)
            latestComponentStatuses[componentID] = max(componentStatus, currentComponentStatus)

            incidentHash = hashIncident(incident)
            if incidentHash in incidentIDs:
                numberOfNewUpdates = len(incident['updates']) - len(getIncidentUpdates(incidentIDs[incidentHash]))
                if numberOfNewUpdates > 0:
                    updateIncident(incidentIDs[incidentHash], incident, numberOfNewUpdates)
                else:
                    log("Info", "Incident {name} with the id {id} is up-to-date".format(name=incident['name'],
                                                                                        id=incidentIDs[incidentHash]
                                                                                    )
                    )
            else:
                createIncident(incident)

    for componentID, latestComponentStatus in latestComponentStatuses.items():
        cachetComponentStatuses = getCachetComponents("id: status")
        if latestComponentStatus != cachetComponentStatuses[componentID]:
            updateComponentStatus(componentID, latestComponentStatus)

    if debug:
        print("Incidents in Cachet before they where updated:")
        pprint(incidentIDs)
        print("\nEnabled Incidents:")
        pprint(incidentFunctions)


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

def getIncidentUpdates(incidentID):
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


if __name__ == "__main__":
    # Update Cachet incidents database
    from pprint import pprint
    debug = True

    CRUDIncidents()


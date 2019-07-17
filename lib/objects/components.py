import json

import requests

from configs import dtadCachetAPI
from configs import APIKey
from enabledProviders import componentFunctions
from lib.utilities.cachet import getCachetComponents
from lib.utilities.tools import log


# Global options
latestComponentStatuses = {}
debug = False


# Main functionality
def CRUDComponents():
    cachetComponentExistences = getCachetComponents("group: {component: False}")
    cachetComponentIDs = getCachetComponents("group: {component: id}")

    # Check which components are already there and mark them accordingly.
    # If a component is not found if will be created.
    for providerName, getComponents in componentFunctions:
        groupName = providerName
        for component in getComponents():
            if component['name'] in cachetComponentExistences[groupName]:
                cachetComponentExistences[groupName][component['name']] = True

                componentID = cachetComponentIDs[groupName][component['name']]
                componentStatus = component['status']
                currentComponentStatus = latestComponentStatuses.get(componentID, 0)
                latestComponentStatuses[componentID] = max(componentStatus, currentComponentStatus)
            else:
                createComponent(component)

    # All components not marked previously will be deleted
    componentIDs = getCachetComponents("group: {component: id}")
    for group in cachetComponentExistences:
        for component in cachetComponentExistences[group]:
            if cachetComponentExistences[group][component] == False:
                deleteComponent(componentIDs[group][component])

    if debug:
        print("Components in Cachet before they where updated:")
        pprint(cachetComponentExistences)
        print("\nEnabled Components:")
        pprint(componentFunctions)
        print("\nComponents to IDs dict:")
        pprint(componentIDs)


# Helper functions
def createComponent(component):
    payload = {}

    payload['name'] = component['name']
    payload['description'] = component['description']
    payload['status'] = component['status']
    payload['group_id'] = component['group_id']
    
    payload['enabled'] = 1

    try:
        response = requests.post("{}/components".format(dtadCachetAPI),
                                data=json.dumps(payload),
                                headers={'X-Cachet-Token': APIKey,
                                         'Content-Type': "application/json"})
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Couldn't create component {name}".format(name=component['name']))
        log("Error", "Unsuccessful HTTP POST Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    else:
        log("Success", "Created the component \"{name}\" at the provider {providerName}".format(
                                                                                    name=component['name'],
                                                                                    providerName=component['provider']
                                                                                )
        )

def updateComponentStatus(componentID, componentStatus):
    payload = {}

    payload['status'] = componentStatus

    try:
        response = requests.put("{dtadCachetAPI}/components/{componentID}".format(
                                                            dtadCachetAPI = dtadCachetAPI,
                                                            componentID = componentID
                                                        ),
                                data = json.dumps(payload),
                                headers = {'X-Cachet-Token': APIKey,
                                           'Content-Type': "application/json"}
                            )
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Couldn't update the status of the component with the id {id}".format(id=componentID))
        log("Error", "Unsuccessful HTTP PUT Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    else:
        log("Success", "Updated the component with the id {id}".format(id=componentID))

def deleteComponent(componentID):
    try:
        response = requests.delete("{dtadCachetAPI}/components/{id}".format(
                                                        dtadCachetAPI=dtadCachetAPI, 
                                                        id=componentID
                                                    ),
                                   headers={'X-Cachet-Token': APIKey}
                                )
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Coulden't delete an object from the endpoint 'components/' !!!")
        log("Error", "Unsuccessful HTTP DELETE Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    else:
        log("Success", "Deleted the component with the id {id}".format(id=componentID))


if __name__ == "__main__":
    # Update Cachet components database
    from pprint import pprint
    debug = True

    CRUDComponents()

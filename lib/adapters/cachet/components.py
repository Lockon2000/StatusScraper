import json

import requests

from configs import dtadCachetAPI
from configs import APIKey
from lib.utilities.tools import log


# Global options
debug = False
objectsPerPage = 100000


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

def readComponents(format="group: {component: id}"):
    result = {}

    try:
        response = requests.get("{dtadCachetAPI}/components?per_page={objectsPerPage}".format(
                                                                            dtadCachetAPI=dtadCachetAPI,
                                                                            objectsPerPage=objectsPerPage
                                                                        )
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Coulden't retrieve the Components from Cachet!!!")
        log("Error", "Unsuccessful HTTP Request! Error Code {}".format(str(e)))

    groups = getCachetGroups("id: group")
    if format == "group: {component: id}":
        for group in groups.values():
            result[group] = {}

        for component in response.json()['data']:
            result[groups[component['group_id']]][component['name']] = component['id']
    elif format == "group: {component: False}":
        for group in groups.values():
            result[group] = {}

        for component in response.json()['data']:
            result[groups[component['group_id']]][component['name']] = False
    elif format == "groupID: {component: id}":
        for groupID in groups:
            result[groupID] = {}

        for component in response.json()['data']:
            result[component['group_id']][component['name']] = component['id']
    elif format == "groupID: {component: False}":
        for groupID in groups:
            result[groupID] = {}

        for component in response.json()['data']:
            result[component['group_id']][component['name']] = False
    elif format == "id: status":
        for component in response.json()['data']:
            result[component['id']] = component['status']

    return result

def updateComponent(componentID, componentStatus):
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

    # Testing readComponents
    print("# readComponents")
    print("## group: {component: id}")
    pprint(readComponents("group: {component: id}"))
    print("## group: {component: False}")
    pprint(readComponents("group: {component: False}"))
    print("## groupID: {component: id}")
    pprint(readComponents("groupID: {component: id}"))
    print("## groupID: {component: False}")
    pprint(readComponents("groupID: {component: False}"))
    print("## id: status")
    pprint(readComponents("id: status"))
    print("------------------\n\n")
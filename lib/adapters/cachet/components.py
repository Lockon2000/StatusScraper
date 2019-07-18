import json

import requests

from conf.configs import API
from conf.configs import APIKey
from lib.internals.utilities.tools import log
from .groups import readGroups


# Global options
objectsPerPage = 100000


def createComponent(component):
    payload = {}

    payload['name'] = component['name']
    payload['description'] = component['description']
    payload['status'] = component['status']
    payload['group_id'] = component['group_id']
    
    payload['enabled'] = 1

    try:
        response = requests.post("{}/components".format(API),
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
        response = requests.get("{API}/components?per_page={objectsPerPage}".format(
                                                                            API=API,
                                                                            objectsPerPage=objectsPerPage
                                                                        )
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Coulden't retrieve the Components from Cachet!!!")
        log("Error", "Unsuccessful HTTP Request! Error Code {}".format(str(e)))

    groups = readGroups("id: group")
    if format == "group: {component: id}":
        for groupID, group in groups.items():
            result[group] = {
                component['name']: component['id']
                for component in response.json()['data']
                if groupID == component['group_id']
            }
    elif format == "group: {component: False}":
        for groupID, group in groups.items():
            result[group] = {
                component['name']: False
                for component in response.json()['data']
                if groupID == component['group_id']
            }
    elif format == "groupID: {component: id}":
        for groupID, group in groups.items():
            result[groupID] = {
                component['name']: component['id']
                for component in response.json()['data']
                if groupID == component['group_id']
            }
    elif format == "groupID: {component: False}":
        for groupID, group in groups.items():
            result[groupID] = {
                component['name']: False
                for component in response.json()['data']
                if groupID == component['group_id']
            }
    elif format == "id: status":
        result = {
            component['id']: component['status']
            for component in response.json()['data']
        }
    elif format == "group: components list":
        for groupID, group in groups.items():
            result[group] = [
                component['name']
                for component in response.json()['data']
                if groupID == component['group_id']
            ]

    return result

def updateComponent(componentID, componentStatus):
    payload = {}

    payload['status'] = componentStatus

    try:
        response = requests.put("{API}/components/{componentID}".format(
                                                            API = API,
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
        response = requests.delete("{API}/components/{id}".format(
                                                        API=API, 
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


import json

import requests

from configs import dtadCachetAPI
from configs import APIKey
from lib.utilities.hashing import hashIncident


# Global options
debug = False
objectsPerPage = 100000


def getCachetGroups(format="group: id"):
    result = {}

    try:
        response = requests.get("{dtadCachetAPI}/components/groups?per_page={objectsPerPage}".format(
                                                                                    dtadCachetAPI=dtadCachetAPI,
                                                                                    objectsPerPage=objectsPerPage
                                                                                )
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Coulden't retrieve the Groups from Cachet!!!")
        log("Error", "Unsuccessful HTTP Request! Error Code {}".format(str(e)))

    if format == "group: id":
        for group in response.json()['data']:
            result[group['name']] = group['id']
    elif format == "id: group":
        for group in response.json()['data']:
            result[group['id']] = group['name']
    elif format == "group: False":
        for group in response.json()['data']:
            result[group['name']] = False

    return result

def getCachetComponents(format="group: {component: id}"):
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

def getCachetIncident(format="incidentHash: id"):
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


if __name__ == '__main__':
    # Test module
    from pprint import pprint
    debug = True

    # Testing getCachetGroups
    print("# getCachetGroups")
    print("## group: id")
    pprint(getCachetGroups("group: id"))
    print("## id: group")
    pprint(getCachetGroups("id: group"))
    print("## group: False")
    pprint(getCachetGroups("group: False"))
    print("------------------\n\n")

    # Testing getCachetComponents
    print("# getCachetComponents")
    print("## group: {component: id}")
    pprint(getCachetComponents("group: {component: id}"))
    print("## group: {component: False}")
    pprint(getCachetComponents("group: {component: False}"))
    print("## groupID: {component: id}")
    pprint(getCachetComponents("groupID: {component: id}"))
    print("## groupID: {component: False}")
    pprint(getCachetComponents("groupID: {component: False}"))
    print("## id: status")
    pprint(getCachetComponents("id: status"))
    print("------------------\n\n")

    # Testing getCachetIncidents
    print("# getCachetIncidents")
    print("## incidentHash: id")
    pprint(getCachetIncident("incidentHash: id"))
    print("## id: status")
    pprint(getCachetIncident("id: status"))
    print("------------------\n\n")

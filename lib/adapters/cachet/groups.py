import json

import requests

from configs import dtadCachetAPI
from configs import APIKey
from lib.utilities.tools import log


# Global options
debug = False
objectsPerPage = 100000


def createGroup(groupName):
    payload = {}

    payload['name'] = groupName

    payload['visible'] = 1      # True
    payload['collapsed'] = 1    # True
                                # 1: always collapsed
                                # 2: collapsed as long as there are no problems

    try:
        response = requests.post("{}/components/groups".format(dtadCachetAPI),
                                data=json.dumps(payload),
                                headers={'X-Cachet-Token': APIKey,
                                         'Content-Type': "application/json"})
        response.raise_for_status()
        return response
    except requests.HTTPError as e:
        log("Error", "Coulden't create the group {}".format(groupName))
        log("Error", "Unsuccessful HTTP POST Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    else:
        log("Success", "Created the group {name}".format(name=groupName))

def readGroups(format="group: id"):
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

def deleteGroup(groupID):
    try:
        response = requests.delete("{dtadCachetAPI}/components/groups/{id}".format(dtadCachetAPI=dtadCachetAPI, id=groupID),
                                   headers={'X-Cachet-Token': APIKey})
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Coulden't delete an object from the endpoint 'components/groups/' !!!")
        log("Error", "Unsuccessful HTTP DELETE Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    else:
        log("Success", "Deleted the group with the id {id}".format(id=groupID))


if __name__ == '__main__':
    # Test module
    from pprint import pprint
    debug = True

    # Testing readGroups
    print("# readGroups")
    print("## group: id")
    pprint(readGroups("group: id"))
    print("## id: group")
    pprint(readGroups("id: group"))
    print("## group: False")
    pprint(readGroups("group: False"))
    print("------------------\n\n")

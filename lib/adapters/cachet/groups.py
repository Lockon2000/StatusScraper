import json

import requests

from conf.configs import API
from conf.configs import APIKey
from lib.internals.utilities.tools import log


# Global options
objectsPerPage = 100000


def createGroup(groupName):
    payload = {}

    payload['name'] = groupName

    payload['visible'] = 1      
    payload['collapsed'] = 1    # 0: never collapsed
                                # 1: always collapsed
                                # 2: collapsed as long as there are no problems

    try:
        response = requests.post("{}/components/groups".format(API),
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
    try:
        response = requests.get("{API}/components/groups?per_page={objectsPerPage}".format(
                                                                                    API=API,
                                                                                    objectsPerPage=objectsPerPage
                                                                                )
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Coulden't retrieve the Groups from Cachet!!!")
        log("Error", "Unsuccessful HTTP Request! Error Code {}".format(str(e)))

    if format == "group: id":
        result = {
            group['name']: group['id']
            for group in response.json()['data']
        }
    elif format == "id: group":
        result = {
            group['id']: group['name']
            for group in response.json()['data']
        }
    elif format == "group: False":
        result = {
            group['name']: False
            for group in response.json()['data']
        }
    elif format == "list":
        result = [
            group['name']
            for group in response.json()['data']
        ]

    return result

def deleteGroup(groupID):
    try:
        response = requests.delete("{API}/components/groups/{id}".format(API=API, id=groupID),
                                   headers={'X-Cachet-Token': APIKey})
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Coulden't delete an object from the endpoint 'components/groups/' !!!")
        log("Error", "Unsuccessful HTTP DELETE Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    else:
        log("Success", "Deleted the group with the id {id}".format(id=groupID))


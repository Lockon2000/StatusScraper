import json

import requests

from configs import dtadCachetAPI
from configs import APIKey
from enabledProviders import modules
from lib.objects.components import deleteComponent
from lib.utilities.cachet import getCachetGroups
from lib.utilities.cachet import getCachetComponents
from lib.utilities.tools import log


# Global options
debug = False


# Main functionality
def CRUDGroups():
    cachetGroups = getCachetGroups("group: False")
    enabledGroups = [module.providerName for module in modules]

    # Check which groups are already there and mark them accordingly.
    # If a group is not found if will be created.
    for group in enabledGroups:
        if group in cachetGroups:
            cachetGroups[group] = True
        else:
            createGroup(group)

    # All groups not marked previously will be deleted
    groupIDs = getCachetGroups("group: id")
    componentIDs = getCachetComponents("group: {component: id}")
    for group in cachetGroups:
        if cachetGroups[group] == False:
            for componentID in componentIDs[group].values():
                deleteComponent(componentID)
            deleteGroup(groupIDs[group])

    if debug:
        print("Groups in Cachet before they where updated:")
        pprint(cachetGroups.keys())
        print("\nEnabled Groups:")
        pprint(enabledGroups)
        print("\nGroups to IDs dict:")
        pprint(groupIDs)
        print("\nComponents to IDs dict:")
        pprint(componentIDs)


# Helper functions
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
    # Update Cachet groups database
    from pprint import pprint
    debug = True

    CRUDGroups()

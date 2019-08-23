from lib.adapters import *
from lib.internals.utilities.incidentIdentification import buildIncidentHash
from lib.internals.utilities.bodyFormatting import deconstructIncidentBody

def reconstructIncident(incident):
    incident.update(deconstructIncidentBody(incident['body']))

# This function first makes a call to the status site to retriev all groups then formats them
# according to the requested format and returns them.
def readFormatedGroups(form="group: ID"):
    # Input:
    #   form: A string with the needed format. Note: 'group' here means group name.
    # Output:
    #   succeeded: Will return a dict or a list with the groups according to the requested format.
    #   failed: Will raise a requests.HTTPError exception or raise a ValueError exception.

    # Read the groups from the status site with the guaranteed pieces of information
    interimResults = readGroups()

    # Decide according to the supplied format which format to return
    if form == "group: ID":
        result = {
            group['name']: group['ID']
            for group in interimResults
        }
    elif form == "ID: group":
        result = {
            group['ID']: group['name']
            for group in interimResults
        }
    elif form == "group: False":
        result = {
            group['name']: False
            for group in interimResults
        }
    elif form == "list":
        result = [
            group['name']
            for group in interimResults
        ]
    else:
        raise ValueError("'{form}' is not a valid format".format(form=form))

    return result

# This function first makes a call to the status site to retriev all components then formats them
# according to the requested format and returns them.
def readFormatedComponents(form="group: {component: ID}", caseSensitivity=True):
    # Input:
    #   form: A string with the needed format. Note: 'group' and 'component' here mean group and component names.
    #   caseSensitivity: A boolean specifying if the retured dict should be a normal dict or a case insensitive one.
    # Output:
    #   succeeded: Will return a dict with the components in the requested format.
    #   failed: Will raise a requests.HTTPError exception or raise a ValueError exception.

    # Read the components from the status site with the guaranteed pieces of information
    interimResults = readComponents()

    # Decide according to the supplied format which format to build
    groups = readFormatedGroups("ID: group")
    result = {}
    if form == "group: {component: ID}":
        for groupID, group in groups.items():
            result[group] = {
                component['name']: component['ID']
                for component in interimResults
                if groupID == component['groupID']
            }
    elif form == "group: {component: False}":
        for groupID, group in groups.items():
            result[group] = {
                component['name']: False
                for component in interimResults
                if groupID == component['groupID']
            }
    elif form == "groupID: {component: ID}":
        for groupID, group in groups.items():
            result[groupID] = {
                component['name']: component['ID']
                for component in interimResults
                if groupID == component['groupID']
            }
    elif form == "groupID: {component: False}":
        for groupID, group in groups.items():
            result[groupID] = {
                component['name']: False
                for component in interimResults
                if groupID == component['groupID']
            }
    elif form == "ID: status":
        result = {
            component['ID']: component['status']
            for component in interimResults
        }
    elif form == "group: components list":
        for groupID, group in groups.items():
            result[group] = [
                component['name']
                for component in interimResults
                if groupID == component['groupID']
            ]
    else:       # The requested format dosen't match any provided format
        raise ValueError("'{form}' is not a valid format".format(form=form))

    # If caseSensitivity is false then supply a case insensitive dict
    if not caseSensitivity:
        # Test whether the results dict contanins nested dicts as they need to be converted too,
        # so get the first value and test it.
        if type(next(iter(result.values()))) == dict:
            # Convert all subdicts.
            for key in result:
                result[key] = CaseInsensitiveDict(result[key])
        # Convert a main dict and return it
        return CaseInsensitiveDict(result)

    # caseSensitivity is true so return a normal case sensitive dict
    return result

# This function first makes a call to the status site to retriev all incidents then formats them
# according to the requested format and returns them.
def readFormatedIncidents(form="hashValue: ID"):
    # Input:
    #   form: A string with the needed format. Note: 'hashValue' here means the unique hashValue of the incident
    #         identifying it.
    # Output:
    #   succeeded: Will return a dict with the incidents in the requested format.
    #   failed: Will raise a requests.HTTPError exception or raise a ValueError exception.

    # Read the incidents from the status site with the guaranteed pieces of information
    interimResults = readIncidents()
    
    # Reconstruct the incidents to the extent possible as the additional information is needed to construct the result.
    for interimResult in interimResults:
        reconstructIncident(interimResult)

    # Decide according to the supplied format which format to build
    if form == "hashValue: ID":
        result = {
            buildIncidentHash(incident): incident['ID']
            for incident in interimResults
        }
    elif form == "ID: status":
        result = {
            incident['ID']: incident['status']
            for incident in interimResults
        }
    else:
        raise ValueError("'{form}' is not a valid format".format(form=form))

    return result

# This funtions counts the number of updates an incident has and returns it
def readNumberOfIncidentUpdates(incidentID):
    # Input:
    #   incidentID: The ID of the incident which updates we want to count.
    # Output:
    #   succeeded: Will return an int representing the number of updates of incident.
    #   failed: Will raise a requests.HTTPError exception.

    # Read the incident updates from the status site with the guaranteed pieces of information
    updates = readIncidentUpdates()

    # Return their number
    return len(updates)


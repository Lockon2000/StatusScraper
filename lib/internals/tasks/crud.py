from importlib import import_module

from conf.config import adapter


# Global options
debug = False

# Global steps
adapterModule = import_module("lib.apdapters."+adapter)
globals().update(
    {k: v for (k, v) in adapterModule.__dict__.items() if not k.startswith('_')
})

# Global variables
latestComponentStatuses = {}


# desc
def CRUD(providers):





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
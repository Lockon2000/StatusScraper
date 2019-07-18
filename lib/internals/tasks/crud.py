from importlib import import_module

from conf.config import adapter


# Global options
debug = False

# Global steps
adapterModule = import_module("lib.apdapters."+adapter)
globals().update(
    {k: v for (k, v) in adapterModule.__dict__.items() if not k.startswith('_')
})


# desc
def CRUD(providers):
    # At the beginning we make sure that there is a group for every enabled provider.
    # If an enabled provider is missing we create a group for it.
    # No groups Are deleted!!! It lies upon the admins to make sure there are no unwanted groups.
    enabledGroups = [module.providerName for module in providers["modules"]]
    ensureGroups(enabledGroups)

    # Now we check the enabled components. Components are enabled if theire provider ist enabled and
    # they are not filtered. Note that we only care for the existence of the components, not their
    # status. So no stauts updates are made. If a component is newly created it will be created with
    # the status found upon scraping.
    # No components Are deleted!!! It lies upon the admins to make sure there are no unwanted components.
    enabledComponents = [*scrapeComponents() for scrapeComponents in providers["componentFunctions"]]
    ensureComponents(enabledComponents)

    # Current enabled component statuses are saved. (This also includes newly created ones)
    latestComponentStatuses = readEnabledComponentStatuses(enabledComponents)

    # Now we get all enabled incidents. Incidents are enabled if theire provider ist enabled and
    # they are not filtered.
    # No incidents are deleted!!! It lies upon the admins to make sure there are no unwanted incidents.
    enabledIncidents = [*scrapeIncidents() for scrapeIncidents in providers["incidentFunctions"]]
    ensureIncidents(enabledIncidents)


# Helper Functions -----------------------------------------------------------------
def ensureGroups(enabledGroups):
    # Get the groups already in the adapter.
    currentGroups = readGroups("list")

    # Check which groups are already there. If a group is not found if will be created.
    for group in enabledGroups:
        if group not in cachetGroups:
            createGroup(group)

def ensureComponents(enabledComponents):
    # Get the components already in the adapter and the components that should be there
    currentComponent = readComponents("group: components list")

    # Check which components are already there. If a component is not found if will be created.
    for component in enabledComponents:
        if component['name'] not in currentComponent[component['provider']]:
            createComponent(component)

def readEnabledComponentStatuses(enabledComponents):
    # Get all component IDs after the components were ensured
    ComponentIDs = readComponents("group: {component: id}")

    result = {}
    for component in enabledComponents:
        componentID = ComponentIDs[component['provider']][component['name']]
        result[componentID] = component['status']

    return result

def ensureIncidents(enabledIncidents):
    for incident in enabledIncidents:





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
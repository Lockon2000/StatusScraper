from lib.utilities.formatting import buildIncidentMessage
from lib.utilities.formatting import buildIncidentUpdateMessage
from lib.utilities.tools import getThenParse
from lib.utilities.wrappers import componentsGetterWrapper
from lib.utilities.wrappers import incidentsGetterWrapper
from lib.utilities.wrappers import maintenancesGetterWrapper
from lib.utilities.cachet import getCachetGroups
from lib.utilities.cachet import getCachetComponents
from lib.utilities.filtering import isRelevantComponent
from lib.utilities.filtering import isRelevantIncident
from lib.utilities.filtering import isRelevantMaintenance
from lib.utilities.hashing import setIncidentMarker


providerName =  
statusURL = 
parsedWebPage = getThenParse(statusURL)

debug = False


# Components Scrapper ----------------------------------------------------------------------
@componentsGetterWrapper(providerName)
def getComponents():
    components = []

    groupIDs = getCachetGroups("group: id")
    componentIDs = getCachetComponents("groupID: {component: id}")
    rawComponents = 

    for rawComponent in rawComponents:
        name = 
        description = 
        verbalStatus = 
        status = convert____ComponentStatus(verbalStatus)
        groupID = groupIDs[providerName]
        componentID = componentIDs.get(groupID, {}).get(name)
        provider = providerName

        component = {
            'name': name,
            'description': description,
            'verbalStatus': verbalStatus,
            'status': status,
            'group_id': groupID,
            'component_id': componentID,
            'provider': provider
        }

        if isRelevantComponent(providerName, component):
            components.append(component)

    return components


# Components Helper Functions --------------------------------------------------------------
# Nothing yet.


# Incidents Scrapper ---------------------------------------------------------------------
@incidentsGetterWrapper(providerName)
def getIncidents():
    incidents = []

    rawIncidents = 

    for rawIncident in rawIncidents:
        name = 
        verbalComponents = 
        description = 
        updates = 
        providerCreatedAt = 
        verbalStatus = 
        status = 
        componentID = 
        componentStatus = 
        locations = 
        provider = providerName
        link = 
        message = buildIncidentMessage(**locals())

        incident = {
            'name': name,
            'message': message,
            'verbalStatus': verbalStatus,
            'status': status,
            'updates': updates,
            'verbalComponents': verbalComponents,
            'component_id': componentID,
            'description': description,
            'component_status': componentStatus,
            'provider_created_at': providerCreatedAt,
            'locations': locations,
            'provider': provider,
            'link': link
        }

        if isRelevantIncident(providerName, incident):
            setIncidentMarker(incident)
            incidents.append(incident)

    return incidents


# Incidents Helper Functions --------------------------------------------------------------
# Nothing yet.


# Maintenances Scrapper --------------------------------------------------------------
def getMaintenances():
    # We are not interested in maintenances right now.
    pass
    # maintenances = []

    # ####### General Scrapping Logic
    # rawMaintenances = 
    # #######

    # for rawMaintenance in rawMaintenances:
    #     ######### Individual Scrapping Logic
    #     name = 
    #     message = 
    #     scheduledAt = 
    #     completedAt = 
    #     components = 
    #     locations = 
    #     #########

    #     maintenance = {
    #         'name': name,
    #         'message': message,
    #         'scheduled_at': scheduledAt,
    #         'completed_at': completedAt,
    #         'components': components,
    #         'locations': locations,
    #     }
    #     maintenances.append(maintenance)

    # return maintenances


# Maintenances Helper Functions --------------------------------------------------------------
# Nothing yet.


# General Helper Functions ----------------------------------------------------------
# Nothing yet.


# Module Testing --------------------------------------------------------------
if __name__ == '__main__':
    # Test this module
    from pprint import pprint
    debug = True

    print("-----------------Components------------------")
    pprint(getComponents())
    print("-----------------Incidents-------------------")
    pprint(getIncidents())
    # print("-----------------Maintenances----------------")
    # pprint(getMaintenances())

from itertools import chain

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


providerName = 'NFON'
statusURL = "https://status.nfon.com"
parsedWebPage = getThenParse(statusURL)

debug = False


# Components Scrapper ----------------------------------------------------------------------
@componentsGetterWrapper(providerName)
def getComponents():
    components = []

    groupIDs = getCachetGroups("group: id")
    componentIDs = getCachetComponents("groupID: {component: id}")
    rawComponents = parsedWebPage.select(".component")

    componentDescription = {
        "Basic Telephony": "Basic telephony, incoming/outgoing calls, phone registration etc.",
        "Secondary Telephony": "Secondary services like conferencing, eFax, voicemail",
        "Administration": "Service portal, CDR portal, mynfon.net",
        "User self care": "NControl, star codes, XML menus etc.",
        "Devices":  "Phone provisioning, FMC, device incidents",
        "PSTN-Termination": "Incoming/Outgoing telephony to/from other carriers/PSTN",
        "Upstream/Peerings": "IP connectivity to the internet and other carriers",
        "Third Party Integration / Value Add Services": "Skype for Business connectors, NMeeting+, voice recording etc."
    }

    for rawComponent in rawComponents:
        name = rawComponent.select(".component_name")[0].text.strip()
        description = componentDescription[name]
        verbalStatus = rawComponent.select(".component-status")[0].text.strip()
        status = convertNfonComponentStatus(verbalStatus)
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

    rawActiveIncidents = parsedWebPage.select("#section_incident_active .page_section")
    rawHistoryIncidents = parsedWebPage.select("#section_main_history .incident")

    for rawIncident in chain(rawActiveIncidents, rawHistoryIncidents):
        provider = providerName
        name = rawIncident.select(".panel-title a")[0].text.strip()
        link = statusURL + rawIncident.select(".panel-title a")[0]['href'].strip()
        verbalComponents = rawIncident.select(".panel-body .row")[1].select(".event_inner_text")[0].text.strip()
        description = scrapIncidentDescription(rawIncident)
        updates = scrapIncidentUpdates(rawIncident)
        providerCreatedAt = updates[0]['date']
        verbalStatus = updates[-1]['verbalStatus']
        status = updates[-1]['status']
        componentID = convertNfonComponents(verbalComponents)
        componentStatus = convertNfonComponentStatus(description, status)
        locations = rawIncident.select(".panel-body .row")[2].select(".event_inner_text")[0].text
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
def scrapIncidentDescription(rawIncident):
    possibility1 = rawIncident.select(".panel-title .incident_status_description")
    possibility2 = rawIncident.select(".panel-title .status_description")

    if possibility1:
        description = possibility1[0].text.strip()
    elif possibility2:
        description = possibility2[0].text.strip()
    else:
        raise Exception("No description scrapped")

    return description

def scrapIncidentUpdates(rawIncident):
    updates = []

    for update in rawIncident.select(".panel-body .row")[4:]:
        rawDate = update.select(".incident_time")[0].text
        endPosition = rawDate.find(" CE")               # find the position of CET or CEST
        date = convertNfonDate(rawDate[:endPosition])
        verbalStatus = update.select("strong")[1].text.strip()[1:-1]
        status = convertNfonIncidentStatus(verbalStatus)
        info = update.select(".incident_message_details")[0].text
        message = buildIncidentUpdateMessage(date, verbalStatus, info)

        updates.append({
            'date': date,
            'verbalStatus': verbalStatus,
            'status': status,
            'info': info,
            'message': message
        })

    return updates

def convertNfonIncidentStatus(verbalStatus):
    if verbalStatus.lower() == 'investigating':
        status = 1
    elif verbalStatus.lower() == 'identified':
        status = 2
    elif verbalStatus.lower() == 'monitoring':
        status = 3
    elif verbalStatus.lower() == 'resolved':
        status = 4
    else:
        status = -1

    return status


# Maintenances Scrapper --------------------------------------------------------------
@maintenancesGetterWrapper(providerName)
def getMaintenances():
    # We are not interested in maintenances right now.
    pass
    # maintenances = []

    # rawMaintenances = parsedWebPage.select("#section_maintenance_scheduled .page_section")

    # for rawMaintenance in rawMaintenances:
    #     ######### Individual Scrapping Logic
    #     name = rawMaintenance.select(".panel-title a")[0].text
    #     message = rawMaintenance.select(".panel-body .row")[3].select(".event_inner_text")[0].text
    #     nfonDate = rawMaintenance.select(".panel-body .row")[0].select(".event_inner_text")[0].text
    #     endPosition = nfonDate.find(" -")
    #     scheduledAt = convertNfonDate(nfonDate[:endPosition])
    #     completedAt = convertNfonDate(nfonDate[:endPosition-5] + nfonDate[endPosition+3:endPosition+8])
    #     components = rawMaintenance.select(".panel-body .row")[1].select(".event_inner_text")[0].text
    #     locations = rawMaintenance.select(".panel-body .row")[2].select(".event_inner_text")[0].text
    #     provider = providerName
    #     #########

    #     maintenance = {
    #         'name': name,
    #         'message': message,
    #         'nfonDate': nfonDate,
    #         'scheduled_at': scheduledAt,
    #         'completed_at': completedAt,
    #         'components': components,
    #         'locations': locations,
    #         'provider': provider
    #     }

    #     if isRelevantMaintenance(providerName, maintenance):
    #         maintenances.append(maintenance)

    # return maintenances


# Maintenances Helper Functions --------------------------------------------------------------
# Nothing yet.


# General Helper Functions ----------------------------------------------------------
def convertNfonComponents(verbalComponents):
    componentIDs = getCachetComponents("group: {component: id}")

    if verbalComponents.find(",") != -1:
        componentID = [componentIDs[providerName][component] for component in verbalComponents.split(", ")][0]
    else:
        component = verbalComponents
        if component in componentIDs[providerName]:
            componentID = componentIDs[providerName][component]
        else:
            componentID = None

    return componentID

def convertNfonComponentStatus(verbalStatus, incidentStatus=1):
    if incidentStatus == 4:
        status = 1
    else:
        if verbalStatus.lower() == 'operational':
            status = 1
        elif verbalStatus.lower() == 'degraded performance':
            status = 2
        elif verbalStatus.lower() == 'partial service disruption':
            status = 3
        elif verbalStatus.lower() == 'service disruption' or verbalStatus.lower() == 'planned maintenance':
            status = 4
        else:
            status = -1

    return status

def convertNfonDate(nfonDate):
    month, day, year, time = nfonDate.split()
    day = day[:-1]

    if month.lower() == "january":
        month = 1
    elif month.lower() == "february":
        month = 2
    elif month.lower() == "march":
        month = 3
    elif month.lower() == "april":
        month = 4
    elif month.lower() == "may":
        month = 5
    elif month.lower() == "june":
        month = 6
    elif month.lower() == "july":
        month = 7
    elif month.lower() == "august":
        month = 8
    elif month.lower() == "september":
        month = 9
    elif month.lower() == "october":
        month = 10
    elif month.lower() == "november":
        month = 11
    elif month.lower() == "december":
        month = 12

    return "{year}-{month}-{day} {time}".format(year=year,month=month,day=day,time=time)


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

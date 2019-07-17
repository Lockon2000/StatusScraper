from datetime import datetime
from datetime import timedelta
from datetime import timezone
import re

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


providerName = "HubSpot"
statusURL = "https://status.hubspot.com"
parsedWebPage = getThenParse(statusURL)

debug = False


# Components Scrapper ----------------------------------------------------------------------
@componentsGetterWrapper(providerName)
def getComponents():
    components = []

    groupIDs = getCachetGroups("group: id")
    componentIDs = getCachetComponents("groupID: {component: id}")
    rawComponents = parsedWebPage.select(".components-section .component-container")

    componentDescription = {
        "HubSpot Marketing Application": "Sämtliche Komponenten der HubSpot-Marketing-Software, auch bekannt als app.hubspot.com.",
        "HubSpot APIs": "Die HubSpot-APIs umfassen die Verbindungen zu den Anwendungen für Kontakte, Analytics, Workflows, Berichte, Formulare und mehr.",
        "Sales Email Tracking": "Die Erfassung und Verarbeitung von Events in HubSpot Sales, inklusive E-Mail-Öffnungen und -Klicks.",
        "CTA Delivery": "Die Darstellung von auf Webseiten, Landing-Pages und andernorts eingebundenen CTAs.",
        "Form Submission Processing":  "Die Erfassung und Verarbeitung von Formulareinsendungen zur Erstellung oder Erweiterung von Kontaktdaten.",
        "Analytics Event Processing": "Die Verarbeitung von Analytics-Events, um sie darzustellen oder in Berichten zu nutzen.",
        "Email Delivery": "Die Zustellung von E-Mails, die an Kontakte oder Listten von HubSpot-Kunden versandt wurden.",
        "Salesforce Sync": "Die Synchronisierung von Kontaktdaten zwischen HubSpot und Salesforce.",
        "Social Media Engagement": "Tracking und Veröffentlichen von Social-Media-Updates.",
        "Mobile": "Mobile HubSpot-App für iOS und Android",
        "HubSpot CRM": "Alle Bildschirme und Komponenten der HubSpot-CRM-Anwendung.",
        "HubSpot Sales": "Eine Reihe von Anwendungen zur Beschleunigung des Vertriebsprozesses.",
        "CMS Content Delivery": "Das Darstellen von Website-Seiten, Landing-Pages, Blogs und E-Mails für alle sämtliche Kundenwebsites, die auf dem HubSpot CMS gehostet werden.",
        "Form Delivery": "Die Darstellung von Formularen auf Webseiten, Landing-Pages und andernorts.",
        "Analytics Event Collection": "Die Erfassung von Analytics-Events, inklusive Seitenaufrufen, E-Mail-Öffnungen, Klicks usw.",
        "List Segmentation": "Die Aktualisierung von Listen in der Listen-Anwendung der HubSpot Marketing-Software",
        "Email Engagement Tracking": "Analytics zu Öffnungs- und Klickraten für E-Mails, die mit HubSpot versandt werden.",
        "Workflows Processing": "Anmeldungen und das Ausführen bestimmter Schritte mit Workflows in HubSpot.",
        "Conversations": "Die Verarbeitung und Zustellung von Nachrichten an den Conversation-Posteingang"
    }

    for rawComponent in rawComponents:
        name = rawComponent.select(".name")[0].text.strip()
        description = componentDescription[name]
        verbalStatus = rawComponent.select(".component-status")[0].text.strip()
        status = convertHubspotComponentStatus(verbalStatus)
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

    rawIncidents = parsedWebPage.select(".incident-container")

    for rawIncident in rawIncidents:
        link = statusURL + rawIncident.select(".incident-title a")[0]['href'].strip()
        parsedIncidentPage = getThenParse(link)

        name = parsedIncidentPage.select(".incident-name")[0].text.strip()
        description = convertIncidentDescription(parsedIncidentPage.select(".incident-name")[0]['class'])
        updates = scrapIncidentUpdates(parsedIncidentPage)
        providerCreatedAt = updates[0]['date']
        verbalStatus = updates[-1]['verbalStatus']
        status = updates[-1]['status']
        verbalComponents = scrapHubspotComponents(parsedIncidentPage.select(".components-affected")[0].text.strip())
        componentID = convertHubspotComponents(verbalComponents)
        componentStatus = convertHubspotComponentStatus(description, status)
        # locations = 
        provider = providerName
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
            # 'locations': locations,
            'provider': provider,
            'link': link
        }

        if isRelevantIncident(providerName, incident):
            setIncidentMarker(incident)
            incidents.append(incident)

    return incidents


# Incidents Helper Functions --------------------------------------------------------------
def convertIncidentDescription(classes):
    for cls in classes:
        if re.search("impact", cls):
            if cls == "impact-minor":
                return 'degraded performance'
            elif cls == "impact-major":
                return 'partial outage'
            elif cls == "impact-critical":
                return 'major outage'
            elif cls == "impact-maintenance":
                return 'maintenance'

def scrapIncidentUpdates(parsedIncidentPage):
    updates = []

    for update in parsedIncidentPage.select(".incident-updates-container .row")[::-1]:
        verbalStatus = update.select(".update-title")[0].text.strip()
        status = convertIncidentStatus(verbalStatus) or updates[-1]['status']
        dateMatch = re.search(r"(?P<month>.{3}) (?P<day>[\d]{2}), (?P<year>[\d]{4}) - (?P<hour>[\d]{2}):(?P<minute>[\d]{2}) EDT",
                                                update.select(".update-timestamp")[0].text)
        date = convertIncidentDate(dateMatch)
        info = update.select(".update-body")[0].text.encode("utf-8")
        message = buildIncidentUpdateMessage(date, verbalStatus, info)

        updates.append({
            'date': date,
            'verbalStatus': verbalStatus,
            'status': status,
            'info': info,
            'message': message
        })

    return updates

def convertIncidentStatus(verbalStatus):
    if verbalStatus.lower() == 'investigating':
        status = 1
    elif verbalStatus.lower() == 'identified':
        status = 2
    elif verbalStatus.lower() == 'monitoring':
        status = 3
    elif verbalStatus.lower() == 'resolved':
        status = 4
    elif verbalStatus.lower() == 'scheduled':
        status = 1
    elif verbalStatus.lower() == 'in progress':
        status = 1
    elif verbalStatus.lower() == 'completed':
        status = 4
    else:
        status = None

    return status

def convertIncidentDate(dateMatch):
    time = datetime(int(dateMatch.group("year")),
                    convertMonthName(dateMatch.group("month")),
                    int(dateMatch.group("day")),
                    int(dateMatch.group("hour")),
                    int(dateMatch.group("minute")),
                    tzinfo=timezone(-timedelta(hours=4)))

    time = time.astimezone(tz=None)

    return "{year}-{month}-{day} {hour}:{minute}".format(year=time.year,
                                                         month=time.month,
                                                         day=time.day,
                                                         hour=time.hour,
                                                         minute=time.minute)

def scrapHubspotComponents(text):
    text = text[24:-1]
    text = text.replace("and ", "")
    return text


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
def convertHubspotComponents(verbalComponents):
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

def convertHubspotComponentStatus(verbalStatus, incidentStatus=1):
    if incidentStatus == 4:
        status = 1
    else:
        if verbalStatus.lower() == 'operational':
            status = 1
        elif verbalStatus.lower() == 'degraded performance':
            status = 2
        elif verbalStatus.lower() == 'partial outage':
            status = 3
        elif verbalStatus.lower() == 'major outage' or verbalStatus.lower() == 'maintenance':
            status = 4
        else:
            status = -1

    return status

def convertMonthName(name):
    if name.lower() == "jan":
        month = 1
    elif name.lower() == "feb":
        month = 2
    elif name.lower() == "mar":
        month = 3
    elif name.lower() == "apr":
        month = 4
    elif name.lower() == "may":
        month = 5
    elif name.lower() == "jun":
        month = 6
    elif name.lower() == "jul":
        month = 7
    elif name.lower() == "aug":
        month = 8
    elif name.lower() == "sep":
        month = 9
    elif name.lower() == "oct":
        month = 10
    elif name.lower() == "nov":
        month = 11
    elif name.lower() == "dec":
        month = 12

    return month


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

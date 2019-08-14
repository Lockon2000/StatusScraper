from itertools import chain
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


providerName = "CloudFlare"
statusURL = "https://www.cloudflarestatus.com"
parsedWebPage = getThenParse(statusURL)

debug = False


# Components Scrapper ----------------------------------------------------------------------
@componentsGetterWrapper(providerName)
def getComponents():
    components = []

    groupIDs = getCachetGroups("group: id")
    componentIDs = getCachetComponents("groupID: {component: id}")
    rawServiceComponents = parsedWebPage.select(".component-container:last-child .child-components-container .component-inner-container")

    for rawComponent in rawServiceComponents:
        name = rawComponent.select(".name")[0].text.strip()
        description = "-"
        verbalStatus = rawComponent.select(".component-status")[0].text.strip()
        status = convertCloudFlareComponentStatus(verbalStatus)
        groupID = groupIDs.get(providerName)
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

    rawEuropeComponent = parsedWebPage.select(".component-container:first-child > .component-inner-container")[0]

    name = rawEuropeComponent.select(".name")[0].text.strip()
    description = "-"
    verbalStatus = rawEuropeComponent.select(".component-status")[0].text.strip()
    if verbalStatus == "Partial Outage" or verbalStatus == "Degraded Performance":
        verbalStatus = "Re-routed"
    status = convertCloudFlareComponentStatus(verbalStatus)
    groupID = groupIDs.get(providerName)
    componentID = componentIDs.get(groupID, {}).get(name)
    provider = providerName

    europeComponent = {
        'name': name,
        'description': description,
        'verbalStatus': verbalStatus,
        'status': status,
        'group_id': groupID,
        'component_id': componentID,
        'provider': provider
    }
    if isRelevantComponent(providerName, component):
        components.append(europeComponent)

    return components


# Components Helper Functions --------------------------------------------------------------


# Incidents Scrapper ---------------------------------------------------------------------
@incidentsGetterWrapper(providerName)
def getIncidents():
    incidents = []

    rawActiveIncidents = parsedWebPage.select(".unresolved-incidents .unresolved-incident")
    rawHistoryIncidents = parsedWebPage.select(".incidents-list .incident-container")

    for rawIncident in chain(rawActiveIncidents, rawHistoryIncidents):
        link = statusURL + rawIncident.select(".incident-title a")[0]['href'].strip()
        parsedIncidentPage = getThenParse(link)

        name = parsedIncidentPage.select(".incident-name")[0].text.strip()
        description = convertIncidentDescription(parsedIncidentPage.select(".incident-name")[0]['class'])
        updates = scrapIncidentUpdates(parsedIncidentPage)
        providerCreatedAt = updates[0]['date']
        verbalStatus = updates[-1]['verbalStatus']
        status = updates[-1]['status']
        if parsedIncidentPage.select(".components-affected"):
            verbalComponents = scrapCloudFlareComponents(parsedIncidentPage.select(".components-affected")[0].text.strip())
            componentID = convertCloudFlareComponents(verbalComponents)
        else:
            verbalComponents = componentID = None
        componentStatus = convertCloudFlareComponentStatus(description, status)
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
            if cls == "impact-none":
                return "operational"
            elif cls == "impact-minor":
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
        dateMatch = re.search(r"(?P<month>.{3}) (?P<day>[\d]{2}), (?P<year>[\d]{4}) - (?P<hour>[\d]{2}):(?P<minute>[\d]{2}) UTC",
                                                update.select(".update-timestamp")[0].text)
        date = convertIncidentDate(dateMatch)
        info = update.select(".update-body")[0].text
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
                    tzinfo=timezone.utc)

    time = time.astimezone(tz=None)

    return "{year}-{month}-{day} {hour}:{minute}".format(year=time.year,
                                                         month=time.month,
                                                         day=time.day,
                                                         hour=time.hour,
                                                         minute=time.minute)

def scrapCloudFlareComponents(text):
    matches = re.search(r"Cloudflare Sites and Services \((.*)\)", text)
    serviceComponents = matches.group(1) if matches else None
    matches = re.search(r"Europe", text)
    if matches:
        return serviceComponents+", Europe"
    else:
        return serviceComponents


# General Helper Functions ----------------------------------------------------------
def convertCloudFlareComponentStatus(verbalStatus, incidentStatus=1):
    if incidentStatus == 4:
        status = 1
    else:
        if verbalStatus.lower() == 'operational':
            status = 1
        elif verbalStatus.lower() == 're-routed':
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

def convertCloudFlareComponents(verbalComponents):
    if verbalComponents == None:
        return None

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
    # print("-----------------Incidents-------------------")
    # pprint(getIncidents())
    # print("-----------------Maintenances----------------")
    # pprint(getMaintenances())

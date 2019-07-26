import re

from lib.utilities.formatting import buildIncidentMessage
from lib.utilities.formatting import buildIncidentUpdateMessage
from lib.utilities.tools import getThenParse
from lib.utilities.cachet import getCachetGroups
from lib.utilities.cachet import getCachetComponents


providerName = 'DomainFactory'
statusURL = "https://status.df.eu"
parsedWebPage = getThenParse(statusURL)

debug = False


# Components Scrapper ----------------------------------------------------------------------
def getComponents():
    # DomainFactory doesn't expose Components at the time being
    components = []

    groupIDs = getCachetGroups("group: id")
    componentIDs = getCachetComponents("groupID: {component: id}")

    name = "Allgemein"
    description = "DomainFactory Mail-Service"
    status = 1
    groupID = groupIDs[providerName]
    componentID = componentIDs.get(groupID, {}).get(name)
    provider = providerName

    generalComponent = {
        'name': name,
        'description': description,
        'status': status,
        'group_id': groupID,
        'component_id': componentID,
        'provider': provider
    }

    components.append(generalComponent)

    return components


# Components Helper Functions --------------------------------------------------------------
# Nothing yet.


# Incidents Scrapper ---------------------------------------------------------------------
def getIncidents():
    incidents = []

    rawIncidents = parsedWebPage.select(".error_block")
    if not rawIncidents:
        return incidents

    componentIDs = getCachetComponents("group: {component: id}")

    for rawIncident in rawIncidents:
        provider = providerName
        name = rawIncident.select("b")[0].text
        link = statusURL
        verbalComponents = "Allgemein"
        description = "Leistungsprobleme"
        updates = scrapIncidentUpdates(rawIncident)
        providerCreatedAt = updates[0]['date']
        status = updates[-1]['status']
        componentID = componentIDs.get(providerName).get('Allgemein')
        componentStatus = convertDomainfactoryComponentStatus(status)
        locations = None
        message = buildIncidentMessage(**locals())

        incident = {
            'name': name,
            'message': message,
            'description': description,
            'status': status,
            'verbalComponents': verbalComponents,
            'component_id': componentID,
            'component_status': componentStatus,
            'provider_created_at': providerCreatedAt,
            'locations': locations,
            'updates': updates,
            'provider': provider,
            'link': link
        }

        incidents.append(incident)

    return incidents


# Incidents Helper Functions ------------------------------------------------
def scrapIncidentUpdates(rawIncident):
    updates = []

    text = rawIncident.select('.fehlertext')[0].text.strip()
    infos = re.split(r"\[Update .*\]", text)
    dates = list(map(convertDomainfactoryDate, [rawIncident.select("b")[1].text, *re.findall(r"\[Update (.*)\]",text)]))

    for info, date in zip(infos, dates):
        verbalStatus = 'Untersuchungen laufen'
        status = 1
        message = buildIncidentUpdateMessage(date, verbalStatus, info)

        updates.append({
            'date': date,
            'verbalStatus': verbalStatus,
            'status': status,
            'info': info,
            'message': message
        })

    if len(rawIncident.select(".leftcol")) == 2:
        date = convertDomainfactoryDate(rawIncident.select("b")[2].text)
        verbalStatus = 'Behoben'
        status = 4
        info = "Problem wurde behoben!."
        message = buildIncidentUpdateMessage(date, verbalStatus, info)

        updates.append({
            'date': date,
            'verbalStatus': verbalStatus,
            'status': status,
            'info': info,
            'message': message
        })

    if debug:
        incidentPieces.append((dates, infos))

    return updates


# General Helper Functions ----------------------------------------------------
def convertDomainfactoryComponentStatus(incidentStatus):
    if incidentStatus == 1:
        status = 2
    elif incidentStatus == 4:
        status = 1

    return status

def convertDomainfactoryDate(domainfactoryDate):
    if domainfactoryDate.find(",") != -1:
        date, time = domainfactoryDate.split(", ")
        day, month, year = date.split(".")
        time = time.split()[0]
    else:
        date, time = domainfactoryDate.split(" ")
        day, month, year = date.split(".")
        time = time.split()[0]

    return "{year}-{month}-{day} {time}".format(year=year,month=month,day=day,time=time)


# Module Testing --------------------------------------------------------------
if __name__ == '__main__':
    # Test this module
    from pprint import pprint
    debug = True

    incidentPieces = []

    print("-----------------Components------------------")
    pprint(getComponents())
    print("-----------------Incidents-------------------")
    pprint(getIncidents())
    pprint(incidentPieces)


from datetime import datetime
from calendar import month_name
from re import search
from itertools import chain
from locale import setlocale
from locale import LC_ALL

from lib.internals.utilities.providerHelpers import getWebpageThenParse
from lib.internals.structures.enums import ComponentStatus
from lib.internals.structures.enums import IncidentStatus
from lib.internals.structures.enums import IncidentUpdateAction


#  Configurations  -----------------------------------------------------------------------------------------------------

# Note: The provider name here will become the group name later, so make sure the formatting is as you want it
# to appear on the status site.
providerName = 'NFON'
# Specifies the type of the provider, e.g. "E-Mail" or "Website"
providerType = 'Website'
statusPageURL = "https://status.nfon.com"
# This variable dictates the language of the incidents and it will be used to set the programmatically generated
# strings (e.g. incident verbal statuses) with the correct language.
providerLanguage = "en_US"
# These are the descriptions as they will appear on the status site.
componentDescriptions = {
    "Basic Telephony": "Basic telephony, incoming/outgoing calls, phone registration etc.",
    "Secondary Telephony": "Secondary services like conferencing, eFax, voicemail",
    "Administration": "Service portal, CDR portal, mynfon.net",
    "User self care": "Cloudya apps, NControl, star codes, XML menus etc.",
    "Devices":  "Phone provisioning, FMC, device incidents",
    "PSTN-Termination": "Incoming/Outgoing telephony to/from other carriers/PSTN",
    "Upstream/Peerings": "IP connectivity to the internet and other carriers",
    "Third Party Integration / Value Add Services": "Skype for Business connectors, NMeeting+, voice recording etc."
}

# Global Variables and Steps -------------------------------------------------------------------------------------------

parsedWebpage = getWebpageThenParse(statusPageURL)
# This is needed so that within this module the locale is set to the provider language as it is very probable
# that language specific proccessing is needed, e.g. `calender.month_name`
setlocale(LC_ALL, providerLanguage+".utf8")


#  Scraping  -----------------------------------------------------------------------------------------------------------

# This function defines a list of scraping functions where every function scrapes one component and returns the required
# information in the specified format. For more information see the docs under providers.
# It lies upon the implementor to make sure ONLY real components are returned and not also other objects which may share
# its format on the provider status page.
# Further more no filtering should take place. This is handled seperatly at another point in the program. The
# implementor should make sure ALL components are scraped.
def getScrapeComponentFunctions():
    rawComponents = parsedWebpage.select(".component")
    
    functions = []
    for rawComponent in rawComponents:
        # This wrapper is here to capture the current `rawComponent` so that the closure `scrapeComponent` can use it.
        def wrapper(rawComponent):
            # This is the function that actually scrapes the component.
            def scrapeComponent():
                # Helper variables
                verbalStatus = rawComponent.select(".component-status")[0].text.strip()

                name = rawComponent.select(".component_name")[0].text.strip()
                status = convertComponentPlainStatus(verbalStatus)

                component = {
                    'name': name,
                    'status': status
                }

                return component
            return scrapeComponent

        functions.append(wrapper(rawComponent))

    return functions

# This function defines a list of scraping functions where every function scrapes one incident and returns the required
# information in the specified format. For more information see the docs under providers.
# It lies upon the implementor to make sure ONLY real incidents are returned and not also other objects which may share
# its format on the provider status page.
# Further more no filtering should take place. This is handled seperatly at another point in the program. The
# implementor should make sure ALL incidents are scraped.
def getScrapeIncidentFunctions():
    # The recent incidents are shown in two locations: the active incidents at the beginning of the page and
    # the history incidents at the end of the pages.
    rawActiveIncidents = parsedWebpage.select("#section_incident_active .page_section")
    rawHistoryIncidents = parsedWebpage.select("#section_main_history .incident")

    functions = []
    for rawIncident in chain(rawActiveIncidents, rawHistoryIncidents):
        # This wrapper is here to capture the current `rawIncident` so that the closure `scrapeComponent` can use it.
        def wrapper(rawIncident):
            # This is the function that actually scrapes the incident.
            def scrapeIncident():
                title = rawIncident.select(".panel-title a")[0].text.strip()
                updates = scrapIncidentUpdates(rawIncident)
                componentNames = rawIncident.select(".panel-body .row")[1].select(".event_inner_text")[0]. \
                                                                                                text.strip().split(", ")
                componentStatuses = scrapComponentStatusesFromIncident(rawIncident, len(componentNames))
                link = statusPageURL + rawIncident.select(".panel-title a")[0]['href'].strip()
                locations = rawIncident.select(".panel-body .row")[2].select(".event_inner_text")[0]. \
                                                                                                text.strip().split(", ")

                incident = {
                    'title': title,
                    'updates': updates,
                    'components': componentNames,
                    'componentStatuses': componentStatuses,
                    'link': link,
                    'locations': locations
                }

                return incident
            return scrapeIncident

        functions.append(wrapper(rawIncident))

    return functions

# This function converts the NFON specific component statuses to the generalized component status enum values
def convertComponentPlainStatus(verbalStatus):
    if verbalStatus.lower() == 'operational':
        status = ComponentStatus.Operational
    elif verbalStatus.lower() == 'degraded performance':
        status = ComponentStatus.PerformanceIssues
    elif verbalStatus.lower() == 'partial service disruption':
        status = ComponentStatus.PartialOutage
    elif verbalStatus.lower() == 'service disruption':
        status = ComponentStatus.MajorOutage
    elif verbalStatus.lower() == 'planned maintenance': # This happens when the component is being maintained.
        status = ComponentStatus.MajorOutage
    else:
        status = ComponentStatus.Unknown

    return status

# This function scrapes the individual updates of the incidents and the returns the required information.  For more 
# information see the docs under providers.
def scrapIncidentUpdates(rawIncident):
    updates = []
    for rawUpdate in rawIncident.select(".panel-body .row")[4:]:
        # Helper variables
        verbalAction = rawUpdate.select("strong")[1].text.strip()[1:-1]
        dateRegEx = search(r"CES?T(?P<month>\w*) (?P<day>\d{1,2}), " \
                           r"(?P<year>\d{4}) (?P<hour>\d{2}):(?P<minute>\d{2}) UTC",
                           rawUpdate.select(".incident_time")[0].text.strip())

        action = convertIncidentUpdatePlainAction(verbalAction)
        date = convertDate(dateRegEx)
        info = rawUpdate.select(".incident_message_details")[0].text.strip()

        updates.append({
            'action': action,
            'date': date,
            'info': info
        })

    return updates

def convertIncidentUpdatePlainAction(verbalAction):
    if verbalAction.lower() == 'investigating':
        action = IncidentUpdateAction.Investigating
    elif verbalAction.lower() == 'identified':
        action = IncidentUpdateAction.Identified
    elif verbalAction.lower() == 'monitoring':
        action = IncidentUpdateAction.Watching
    elif verbalAction.lower() == 'resolved':
        action = IncidentUpdateAction.Fixed
    elif verbalAction.lower() == 'update':
        action = IncidentUpdateAction.Update
    else:
        action = IncidentUpdateAction.Unknown

    return action

def scrapComponentStatusesFromIncident(rawIncident, numberOfComponents):
    # This is found in the active incidents.
    firstPossibleLocation = rawIncident.select(".panel-title .incident_status_description")
    # This is found in the History.
    secondPossibleLocation = rawIncident.select(".panel-title .status_description")

    if firstPossibleLocation:
        verbalStatus = firstPossibleLocation[0].text.strip()
    elif secondPossibleLocation:
        verbalStatus = secondPossibleLocation[0].text.strip()
    else:
        verbalStatus = "Unknown"
    
    status = convertComponentPlainStatus(verbalStatus)
    statuses = [status for _ in range(numberOfComponents)]

    return statuses

def convertDate(dateRegEx):
    year = int(dateRegEx.group('year'))
    month = list(month_name).index(dateRegEx.group('month'))
    day = int(dateRegEx.group('day'))
    hour = int(dateRegEx.group('hour'))
    minute = int(dateRegEx.group('minute'))

    return datetime(year, month, day, hour, minute)


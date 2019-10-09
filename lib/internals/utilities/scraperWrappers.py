from functools import wraps

from lib.internals.utilities.filtering import isRelevantComponent
from lib.internals.utilities.filtering import isRelevantIncident
from lib.internals.structures.exceptions import IrrelevantComponent
from lib.internals.structures.exceptions import IrrelevantIncident
from lib.internals.utilities.adapterInterface import readFormatedGroups
from lib.internals.utilities.adapterInterface import readFormatedComponents
from lib.internals.utilities.adapterInterface import readFormatedIncidents
from lib.internals.structures.dicts import germanComponentVerbalStatuses
from lib.internals.structures.dicts import englishComponentVerbalStatuses
from lib.internals.structures.dicts import germanIncidentVerbalStatuses
from lib.internals.structures.dicts import englishIncidentVerbalStatuses
from lib.internals.utilities.incidentIdentification import buildIncidentHash
from lib.internals.utilities.incidentIdentification import setIncidentMarker
from lib.internals.structures.enums import IncidentStatus
from lib.internals.utilities.bodyFormatting import constructIncidentBody
from lib.internals.utilities.bodyFormatting import constructIncidentUpdateBody


# Global variables and steps
groupIDs = readFormatedGroups("group: ID")
componentIDs = readFormatedComponents("group: {component: ID}")
incidentIDs = readFormatedIncidents("hashValue: ID")


def scrapeComponentWrapper(providerModule):
    def decorator(scrapeFunction):
        @wraps(scrapeFunction)
        def wrapper():
            # Try to scrape the component from the provider
            try:
                interimResult = scrapeFunction()
            except Exception as e:
                e.providerModule = providerModule
                raise e

            # Check if this component should be filtred
            if not isRelevantComponent(providerModule.providerName, interimResult):
                raise IrrelevantComponent(interimResult)
            
            # Complete needed data according to the specification
            group = providerModule.providerName     # The group name is equal to the configured provider name
            provider = providerModule.providerName
            name = interimResult["name"]
            status = interimResult["status"]
            ID = componentIDs.get(group).get(name)
            verbalStatus = germanComponentVerbalStatuses.get(status)
            description = providerModule.componentDescriptions.get(name)
            groupID = groupIDs.get(group)

            completedComponent = {
                'name': name,
                'group': group,
                'ID': ID,
                'status': status,
                'verbalStatus': verbalStatus,
                'description': description,
                'groupID': groupID,
                'provider': provider
            }

            return completedComponent
        return wrapper
    return decorator

def scrapeIncidentWrapper(providerModule):
    def decorator(scrapeFunction):
        @wraps(scrapeFunction)
        def wrapper():
            # Try to scrape the incident from the provider
            try:
                interimResult = scrapeFunction()
            except Exception as e:
                e.providerModule = providerModule
                raise e

            # Check if this incident should be filtred
            if not isRelevantIncident(providerModule.providerName, interimResult):
                raise IrrelevantIncident(interimResult)
            
            # First complete the incident updates in place

            # Helper variables
            incidentHashValue = buildIncidentHash(interimResult)
            incidentID = incidentIDs.get(incidentHashValue)

            for index, update in enumerate(interimResult['updates']):
                try:
                    incidentStatus = IncidentStatus(update['action'].value)
                except ValueError:
                    incidentStatus = interimResult['updates'][index-1]['incidentStatus']
                body = constructIncidentUpdateBody(update)

                update['incidentID'] = incidentID
                update['incidentStatus'] = incidentStatus
                update['body'] = body

            
            # Complete needed data according to the specification
            provider = providerModule.providerName
            language = providerModule.providerLanguage
            title = interimResult['title']
            updates = interimResult['updates']
            components = interimResult['components']
            componentStatuses = interimResult['componentStatuses']
            link = interimResult['link']
            locations = interimResult['locations']
            ID = incidentID
            hashValue = incidentHashValue
            status = updates[-1]['incidentStatus']
            if language == "de_DE":
                verbalStatus = germanIncidentVerbalStatuses.get(status)
                componentVerbalStatuses = list(map(lambda componentStatus: 
                                                                germanComponentVerbalStatuses.get(componentStatus),
                                                   componentStatuses))
            else:
                verbalStatus = englishIncidentVerbalStatuses.get(status)
                componentVerbalStatuses = list(map(lambda componentStatus: 
                                                                englishComponentVerbalStatuses.get(componentStatus),
                                                   componentStatuses))
            body = constructIncidentBody(**locals())
            creationDate = updates[0]['date']
            lastUpdateDate = updates[-1]['date']

            completedIncident = {
                'provider': provider,
                'language': language,
                'title': title,
                'updates': updates,
                'components': components,
                'componentStatuses': componentStatuses,
                'link': link,
                'locations': locations,
                'ID': ID,
                'hashValue': hashValue,
                'status': status,
                'verbalStatus': verbalStatus,
                'componentVerbalStatuses': componentVerbalStatuses,
                'body': body,
                'creationDate': creationDate,
                'lastUpdateDate': lastUpdateDate
            }

            # Embed the marker in the incident
            setIncidentMarker(completedIncident)

            return completedIncident
        return wrapper
    return decorator


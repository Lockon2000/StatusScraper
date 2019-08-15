from re import search
from re import findall
from re import IGNORECASE

from conf.blacklist import componentsBlacklist
from conf.blacklist import incidentsBlacklist


def isRelevantComponent(provider, component):
    regExParts = componentsBlacklist.get(provider)
    if not regExParts:
        return True

    regEx = "|".join(regExParts)
    string = component['name']

    if regEx:
        if search(regEx, string, IGNORECASE):
            return False

    return True

def isRelevantIncident(provider, incident):
    regExParts = incidentsBlacklist.get(provider)
    if not regExParts:
        regExParts = componentsBlacklist.get(provider)
        if not regExParts:
            return True

        regEx = "|".join(regExParts)
        string = " ".join(incident['verbalComponents'])

        if regEx:
            if len(findall(regEx, string, IGNORECASE)) == len(incident['verbalComponents']):
                return False
    
    regEx = "|".join(regExParts)
    string = incident['title']

    if regEx:
        if search(regEx, string, IGNORECASE):
            return False

    regExParts = componentsBlacklist.get(provider)
    if not regExParts:
        return True

    regEx = "|".join(regExParts)
    string = " ".join(incident['verbalComponents'])

    if regEx:
        if len(findall(regEx, string, IGNORECASE)) == len(incident['verbalComponents']):
            return False

    return True


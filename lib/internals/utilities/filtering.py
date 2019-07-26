from re import search
from re import IGNORECASE

from configs import componentsBlacklist
from configs import incidentsBlacklist


# Global options
debug = False


def isRelevantComponent(component):
    regex = "|".join(componentsBlacklist[component['provider']])
    string = component['name']

    if regex:
        if search(regex, string, IGNORECASE):
            return False

    return True

def isRelevantIncident(incident):
    regex = "|".join(incidentsBlacklist[incident['provider']])
    string = incident['name']

    if regex:
        if search(regex, string, IGNORECASE):
            return False

    regex = "|".join(componentsBlacklist[incident['provider']])
    string = " ".join(incident['verbalComponents'])

    if regex:
        if len(findall(regex, string, IGNORECASE)) == len(incident['verbalComponents']):
            return False

    return True


if __name__ == '__main__':
    # Test module
    from pprint import pprint
    debug = True


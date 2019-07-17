from re import search
from re import IGNORECASE

from configs import componentsBlacklist
from configs import incidentsBlacklist
from configs import maintenancesBlacklist


# Global options
debug = False


def isRelevantComponent(providerName, component):
    regex = "|".join(componentsBlacklist[providerName])
    string = component['name']

    if regex:
        if search(regex, string, IGNORECASE):
            decision = False
        else:
            decision = True
    else:
        decision = True

    return decision

def isRelevantIncident(providerName, incident):
    decision = True

    regex = "|".join(incidentsBlacklist[providerName])
    string = incident['name']

    if regex:
        if search(regex, string, IGNORECASE):
            decision = False

    regex = "|".join(componentsBlacklist[providerName])
    string = incident['verbalComponents']

    if regex:
        if search(regex, string, IGNORECASE):
            decision = False

    return decision

def isRelevantMaintenance(providerName, maintenance):
    regex = "|".join(maintenancesBlacklist[providerName])
    string = maintenance['name']

    if regex:
        if search(regex, string, IGNORECASE):
            decision = False
        else:
            decision = True
    else:
        decision = True

    return decision


if __name__ == '__main__':
    # Test module
    from pprint import pprint
    debug = True

    from enabledProviders import modules
    providerNames = [module.providerName for module in modules]
    print("### Relevance Functions RegExes")
    for providerName in providerNames:
        print("\n----------RegEx's for provider {} ----------".format(providerName))
        print("Components RegEx", "|".join(componentsBlacklist[providerName]))
        print("Incidents RegEx", "|".join(incidentsBlacklist[providerName]))
        print("Maintenances RegEx", "|".join(maintenancesBlacklist[providerName]))

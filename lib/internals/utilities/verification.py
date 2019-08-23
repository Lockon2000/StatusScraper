from lib.internals.utilities.logging import log
from conf.configs import *

def verifyConfigurations():
    globalSymboleTable = globals()
    requiredConfigs = [
        {'name':"adapter", 'type':str},
        {'name':"API", 'type':str},
        {'name':"APIKey", 'type':str},
        {'name':"logPath", 'type':str},
        {'name':"logFiles", 'type':list},
        {'name':"enabledProviders", 'type':list},
        {'name':"manualComponents", 'type':list}
    ]
    for requiredConfig in requiredConfigs:
        if requiredConfig['name'] not in globalSymboleTable:
            log.error("Faulty configurations: {name} is missing!".format(name=requiredConfig['name']))
            return False
        elif requiredConfig['type'] is not type(globalSymboleTable[requiredConfig['name']]):
            log.error("Faulty configurations: {name} has incorrect type!".format(name=requiredConfig['name']))
            return False
    
    # All required configurations are present and have correct type
    return True

def verifyAdapter(adapter=adapter):
    return True
    
def verifyProviders(providers=enabledProviders):
    return True
    

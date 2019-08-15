from importlib import import_module

from lib.internals.utilities.verification import verifyConfigurations
from lib.internals.utilities.verification import verifyAdapters
from lib.internals.utilities.verification import verifyProviders
from lib.internals.utilities.logging import setupLogging
from lib.internals.utilities.scraperWrappers import componentsGetterWrapper
from lib.internals.utilities.scraperWrappers import incidentsGetterWrapper
from conf.configs import enabledProviders


# The init function initialises the Program by taking all necessary steps to ensure a successful run of the 
# program and it returns the necessary variables for the further execution of the program. It guarantees that 
# if it runs successfully that the program will not come to an abrupt end.
def init():
    # Insurances:
    setupLogging()

    # Verifications:
    verifyConfigurations()
    verifyAdapters()
    verifyProviders()

    # Needed variables for the CRUD function:
    providers = {
        "modules":[
            import_module("lib.providers."+provider.lower())      # lower cased providers to provide for
            for provider in enabledProviders                      # case insensitve configuration
        ]
    }

    providers.update({
        "componentFunctions": [
            componentsGetterWrapper(module.providerName)(module.getComponents)
            for module in providers["modules"]
        ],
        "incidentFunctions": [
            incidentsGetterWrapper(module.providerName)(module.getIncidents)
            for module in providers["modules"]
        ]
    })

    return providers
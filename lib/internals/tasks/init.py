from lib.internals.utilities.verfication import verifyConfigurations
from lib.internals.utilities.verfication import verifyAdapters
from lib.internals.utilities.verfication import verifyProviders
from lib.internals.utilities.insurance import insureLogging
from conf.config import enabledProviders


# The init function initialises the Program by taking all necessary steps to ensure a successful run of the 
# program and it returns the necessary variables for the further execution of the program. It guarantees that 
# if it runs successfully that the program will not come to an abrupt end.
def init():
    # Verifications:
    verifyConfigurations()
    verifyAdapters()
    verifyProviders()


    # Insurances:
    insureLogging()

    # Needed variables for the CRUD function:
    providers = {
        "modules":[
            importlib.import_module("lib.providers."+provider)
            for provider in enabledProviders
        ]
    }

    providers.update({
        "componentFunctions": [
            (module.providerName, module.getComponents)
            for module in providers["modules"]
        ],
        "incidentFunctions": [
            (module.providerName, module.getIncidents)
            for module in providers["modules"]
        ]
    })

    return providers
import sys
from importlib import import_module

from lib.internals.utilities.logging import log
from lib.internals.utilities.verification import verifyConfigurations
from lib.internals.utilities.verification import verifyAdapter
from lib.internals.utilities.verification import verifyProviders


# The start function verifies all modular parts (configurations, adapters, providers) of the program and lays any
# needed groundwork, if needed.
# It guarantees that if it runs successfully, then the program will not come to an abrupt end.
def start():
    # Verifications:
    configurationsIntegrity = verifyConfigurations()
    adapterIntegrity = verifyAdapter()
    providersIntergrity = verifyProviders()

    if not all([configurationsIntegrity, adapterIntegrity, providersIntergrity]):
        log.critical("The integrity of the modular parts could not be established. The program will exit!")
        sys.exit(1)
    else:
        log.info("The integrity of the modular parts was extablished.")
    
    # The start function didn't encounter any errors.
    log.info("The start procedure finished succesfully!")
    return
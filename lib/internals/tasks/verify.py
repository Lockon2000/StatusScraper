import sys
from importlib import import_module

from lib.internals.utilities.modularsVerification import verifyConfigurations
from lib.internals.utilities.modularsVerification import verifyAdapter
from lib.internals.utilities.modularsVerification import verifyProviders


# The verify function verifies all modular parts (configurations, adapters, providers) of the program.
# It tries to guarantee that if it runs successfully, then the program will not come to an abrupt end.
def verify():
    # At this point we can't be sure whether logging and the program as a whole are appropriatly configured,
    # so only basic logging can be used.
    from lib.internals.utilities.basicLogging import log
    configurationsIntegrity = verifyConfigurations(log=log)

    if not configurationsIntegrity:
        log.critical("The integrity of the configurations could not be established. The program will exit!")
        sys.exit(1)
    
    # At this point we have the neccesary information to setup the normal/advanced logging.
    from lib.internals.utilities.advancedLogging import log
    log.info("The configurations have been verified")

    from lib.internals.utilities.configurationsInterface import adapter
    from lib.internals.utilities.configurationsInterface import enabledProviders
    adapterIntegrity = verifyAdapter(adapter, log=log)
    providersIntergrity = verifyProviders(enabledProviders, log=log)

    if not all([adapterIntegrity, providersIntergrity]):
        log.critical("The integrity of the modular parts could not be established. The program will exit!")
        sys.exit(1)
    
    log.info("The configured adapter has been verified")
    log.info("The enabled providers have been verified")
    
    # All tests passed
    log.info("The integrity of the modular parts was established")
    return


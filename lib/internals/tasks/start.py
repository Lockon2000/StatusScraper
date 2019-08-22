from importlib import import_module

from lib.internals.utilities.logging import setupLogging
from lib.internals.utilities.verification import verifyConfigurations
from lib.internals.utilities.verification import verifyAdapters
from lib.internals.utilities.verification import verifyProviders


# The start function setups the needed utilities, e.g. logging, and verifies the configurations and implementations
# supplied to the Program by the administrators and developers.
# It guarantees that if it runs successfully, then the program will not come to an abrupt end.
def start():
    # Insurances:
    setupLogging()

    # Verifications:
    verifyConfigurations()
    verifyAdapters()
    verifyProviders()


from sys import exc_info
from traceback import print_tb
from functools import wraps

from configs import logFile
from lib.utilities.tools import log
from lib.utilities.filtering import isRelevantComponent
from lib.utilities.filtering import isRelevantIncident
from lib.utilities.hashing import setIncidentMarker


# Global options
debug = False


def componentsGetterWrapper(providerName):
    def decorator(func):
        @wraps(func)
        def wrapper():
            try:
                interimResults = func()
            except Exception as e:
                exceptionType, exception, traceback = exc_info()
                log("Error", "Gathering components of \"{providerName}\" failed! Exception {name}: {description}".format(
                                                                            providerName=providerName,
                                                                            name=exceptionType.__name__,
                                                                            description=exception
                                                                        )
                )
                with open(logFile, "a") as file:
                    print_tb(traceback, file=file)
                    print("\n")
                raise e

            results = [
                component
                for component in interimResults
                if isRelevantComponent(component)
            ]

            if results:
                log("Success", "Components found at \"{providerName}\"! {components}".format(providerName=providerName,
                                                                                      components=results
                                                                                    )
                )
            else:
                log("Info", "No Components at \"{providerName}\"".format(providerName=providerName))

            return results
        return wrapper
    return decorator

def incidentsGetterWrapper(providerName):
    def decorator(func):
        @wraps(func)
        def wrapper():
            try:
                interimResults = func()
            except Exception as e:
                exceptionType, exception, traceback = exc_info()
                log("Error", "Gathering incidents of \"{providerName}\" failed! Exception {name}: {description}".format(
                                                                            providerName=providerName,
                                                                            name=exceptionType.__name__,
                                                                            description=exception
                                                                        )
                )
                with open(logFile, "a") as file:
                    print_tb(traceback, file=file)
                    print("\n")
                raise e

            results = [
                setIncidentMarker(incident)
                for incident in interimResults
                if isRelevantIncident(incident)
            ]

            if results:
                log("Success", "Incidents found at \"{providerName}\"! {incidents}".format(providerName=providerName,
                                                                                    incidents=results
                                                                                )
                )
            else:
                log("Info", "No incidents at \"{providerName}\"".format(providerName=providerName))

            return results
        return wrapper
    return decorator


if __name__ == '__main__':
    # Test module
    from pprint import pprint
    debug = True

    pprint("No Tests yet!")

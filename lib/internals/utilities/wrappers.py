from sys import exc_info
from traceback import print_tb
from functools import wraps

from configs import logFile
from lib.utilities.tools import log


# Global options
debug = False


def componentsGetterWrapper(providerName):
    def decorator(func):
        @wraps(func)
        def wrapper():
            try:
                results = func()
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
                results = func()
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

def maintenancesGetterWrapper(providerName):
    def decorator(func):
        @wraps(func)
        def wrapper():
            try:
                results = func()
            except Exception as e:
                exceptionType, exception, traceback = exc_info()
                log("Error", "Gathering maintenances of \"{providerName}\" failed! Exception {name}: {description}".format(
                                                                            providerName=providerName,
                                                                            name=exceptionType.__name__,
                                                                            description=exception
                                                                        )
                )
                with open(logFile, "a") as file:
                    print_tb(traceback, file=file)
                    print("\n")
                raise e

            if results:
                log("Success", "Maintenances found at \"{providerName}\"! {maintenances}".format(providerName=providerName,
                                                                                          maintenances=results
                                                                                        )
                )
            else:
                log("Info", "No maintenances at \"{providerName}\"".format(providerName=providerName))

            return results
        return wrapper
    return decorator


if __name__ == '__main__':
    # Test module
    from pprint import pprint
    debug = True

    pprint("No Tests yet!")

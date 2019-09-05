import os
from importlib import import_module


def verifyConfigurations(*, log):
    # Variables for the different configuration types to be tested.
    requiredConfigurations = []
    optionalConfigurations = []

    # Considering "conf/configs.py": 
    # Note that it is guaranteed at this point that "conf/configs.py" does exist. This is the case because the script 
    # "statusscraper.sh" will have stopped otherwise.

    # Try to import the configs module and make it accessible with the variable module
    try:
        module = import_module("conf.configs")
    except:
        log.exception("Some error occured while trying to import conf/configs.py")
        return False

    # Make all attributes of module directly accessible (Simulation for "from <module> import *")
    globals().update(
                {n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') 
                else 
                {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')}
            )

    requiredConfigurations.extend([
        {'name':"adapter", 'type':str},
        {'name':"APIBaseURL", 'type':str},
        {'name':"APIKey", 'type':str},
        {'name':"logPath", 'type':str},
        {'name':"logFiles", 'type':list},
        {'name':"enabledProviders", 'type':list},
        {'name':"manualComponents", 'type':list}
    ])
    optionalConfigurations.extend([
        # Empty for the time being.
    ])


    # Considering "conf/blacklist.py".
    if os.path.isfile("conf/blacklist.py"):
        # Try to import the blacklist module and make it accessible with the variable module
        try:
            module = import_module("conf.blacklist")
        except:
            log.exception("Some error occured while trying to import conf/blacklist.py")
            return False

        # Make all attributes of module directly accessible (Simulation for "from <module> import *")
        globals().update(
                    {n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') 
                    else 
                    {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')}
                )

        requiredConfigurations.extend([
            # Empty for the time being.
        ])
        optionalConfigurations.extend([
            {'name':"componentsBlacklist", 'type':dict},
            {'name':"incidentsBlacklist", 'type':dict}
        ])
    else:
        # This is an optional file!
        log.debug("No conf/blacklist.py File found!")

    # Storing the global symbole table to see what have been imported.
    globalSymboleTable = globals()

    # Checking the imported variables.
    for configuration in requiredConfigurations:
        if configuration['name'] not in globalSymboleTable:
            log.error("Faulty configurations: {name} is missing!".format(name=configuration['name']))
            return False
        elif configuration['type'] is not type(globalSymboleTable[configuration['name']]):
            log.error("Faulty configurations: {name} has incorrect type!".format(name=configuration['name']))
            return False
    for configuration in optionalConfigurations:
        if configuration['name'] in globalSymboleTable:
            if configuration['type'] is not type(globalSymboleTable[configuration['name']]):
                log.error("Faulty configurations: {name} has incorrect type!".format(name=configuration['name']))
                return False

    # All required configurations are present and have correct type.
    return True

def verifyAdapter(adapter, *, log):
    # For the time being we only check if the folder of the adapter exists and can be imported. More thorough testing
    # will follow.

    # Test if a directory with the adapter name exists at the appropriate place
    if not os.path.isdir("lib/adapters/{adapter}".format(adapter=adapter)):
        log.error("Faulty configurations: There is no module for {adapter} in lib/adapters".format(adapter=adapter))
        return False

    # Try to import the adapters module
    try:
        import_module("lib.adapters."+adapter)
    except:
        log.exception("Some error occured while trying to import lib/adapters/{adapter}".format(adapter=adapter))
        return False
    
    # The adapter passed the tests
    return True
    
def verifyProviders(providers, *, log):
    # For the time being we only check if the files of the providers exist and can be imported. More thorough testing
    # will follow.

    for provider in providers:
        # Test if a file with the provider name exists at the appropriate place
        if not os.path.exists("lib/providers/{provider}.py".format(provider=provider)):
            log.error("Faulty configurations: There is no module for {provider} in lib/providers" \
                                                                                .format(provider=provider))
            return False

        # Try to import the provider module
        try:
            import_module("lib.providers."+provider)
        except:
            log.exception("Some error occured while trying to import lib/providers/{provider}.py" \
                                                                                    .format(provider=provider))
            return False
    
    # The providers passed the tests
    return True
    

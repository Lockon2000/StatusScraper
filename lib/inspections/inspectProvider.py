from sys import argv
from sys import exit
from importlib import import_module
from pprint import pprint

from conf.configs import enabledProviders
from lib.internals.utilities.scraperWrappers import scrapeComponentWrapper
from lib.internals.utilities.scraperWrappers import scrapeIncidentWrapper
from lib.internals.structures.exceptions import IrrelevantComponent
from lib.internals.structures.exceptions import IrrelevantIncident


# Presteps
## This is needed in order to make it possible to specify the inspected providers from the command line.
## If they are not specified on the command line the configured ones in configs.py will be taken as default.
if len(argv) >= 2:
    for argument in argv[1:]:
        if argument.find(",") != -1:
            print("Do not supply the providers as a comma seperated list! But as a space delimited list.")
            exit(1)
    providers = argv[1:]
else:
    providers = enabledProviders

modules = [
    import_module("lib.providers."+provider.lower())        # lower cased providers to provide for
    for provider in providers                               # case insensitve configuration
]

# Inspection
for module in modules:
    print("======= Inspection of Provider {provider} =======\n".format(provider=module.providerName))

    print("= Components:")
    componentScraperFunctions = [
        scrapeComponentWrapper(module)(scrapeComponent)
        for scrapeComponent in module.getScrapeComponentFunctions()
    ]

    components = []
    for scrapeFunction in componentScraperFunctions:
        try:
            component = scrapeFunction()
        except IrrelevantComponent as e:
            e.args[0]["WARNING"] = "This component was deemed irrelevant!"
            components.append(e.args[0])
        else:
            components.append(component)

    pprint(components)

    print("= Incidents:")
    incidentScraperFunctions = [
        scrapeIncidentWrapper(module)(scrapeIncident)
        for scrapeIncident in module.getScrapeIncidentFunctions()
    ]

    incidents = []
    for scrapeFunction in incidentScraperFunctions:
        try:
            incident = scrapeFunction()
        except IrrelevantIncident as e:
            e.args[0]["WARNING"] = "This incident was deemed irrelevant!"
            incidents.append(e.args[0])
        else:
            incidents.append(incident)

    pprint(incidents)


from importlib import import_module

from lib.internals.utilities.configurationsInterface import enabledProviders
from lib.internals.utilities.scraperWrappers import scrapeComponentWrapper
from lib.internals.utilities.scraperWrappers import scrapeIncidentWrapper


def extract():
    modules = [
        import_module("lib.providers."+provider)
        for provider in enabledProviders
    ]

    scrapingProcedures = {
        "components": [
            scrapeComponentWrapper(module)(scrapeComponentFunction)
            for module in modules
            for scrapeComponentFunction in module.getScrapeComponentFunctions()
        ],
        "incidents": [
            scrapeIncidentWrapper(module)(scrapeIncidentFunction)
            for module in modules
            for scrapeIncidentFunction in module.getScrapeIncidentFunctions()
        ]
    }

    preparationProcedures = None
    cleanupProcedures = None

    return scrapingProcedures, preparationProcedures, cleanupProcedures


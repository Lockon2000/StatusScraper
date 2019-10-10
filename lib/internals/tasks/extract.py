from importlib import import_module

from lib.internals.utilities.configurationsInterface import enabledProviders
from lib.internals.utilities.scraperWrappers import scrapeComponentFunctionWrapper
from lib.internals.utilities.scraperWrappers import scrapeIncidentFunctionWrapper


def extract():
    providerModules = [
        import_module("lib.providers."+provider)
        for provider in enabledProviders
    ]

    scrapingProcedures = {
        "components": [
            scrapeComponentFunctionWrapper(providerModule)(scrapeComponentFunction)
            for providerModule in providerModules
            for scrapeComponentFunction in providerModule.getScrapeComponentFunctions()
        ],
        "incidents": [
            scrapeIncidentFunctionWrapper(providerModule)(scrapeIncidentFunction)
            for providerModule in providerModules
            for scrapeIncidentFunction in providerModule.getScrapeIncidentFunctions()
        ]
    }

    preparationProcedures = None
    cleanupProcedures = None

    return scrapingProcedures, preparationProcedures, cleanupProcedures


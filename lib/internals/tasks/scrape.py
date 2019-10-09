from lib.internals.utilities.advancedLogging import log


def scrape(scrapingProcedures):
    data = {"components": [], "incidents": []}

    for scrapeComponent in scrapingProcedures["components"]:
        try:
            component = scrapeComponent()
        except Exception as e:
            log.error("Couldn't scrape one of the components at {providerName}".format(
                                                                    providerName=e.providerModule.providerName
                                                                )
                     )
        data["components"].append(component)

    for scrapeIncident in scrapingProcedures["incidents"]:
        try:
            incident = scrapeIncident()
        except Exception as e:
            log.error("Couldn't scrape one of the incidents at {providerName}".format(
                                                                    providerName=e.providerModule.providerName
                                                                )
                     )
        data["incidents"].append(incident)

    return data
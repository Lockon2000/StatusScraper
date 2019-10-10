from lib.internals.utilities.advancedLogging import log
from lib.internals.structures.exceptions import IrrelevantComponent
from lib.internals.structures.exceptions import IrrelevantIncident


def scrape(scrapingProcedures):
    data = {"components": [], "incidents": []}

    for scrapeComponent in scrapingProcedures["components"]:
        try:
            component = scrapeComponent()
        except IrrelevantComponent as e:
            log.info("A component was deemed irrelevant and therefore skipped! Name: {name}".format(
                                                                                        name=e.component['name']
                                                                                    )
                    )
            continue
        except Exception as e:
            log.error("Couldn't scrape one of the components at {providerName}".format(
                                                                    providerName=e.providerModule.providerName
                                                                )
                     )
            continue
        data["components"].append(component)

    for scrapeIncident in scrapingProcedures["incidents"]:
        try:
            incident = scrapeIncident()
        except IrrelevantIncident as e:
            log.info("An incident was deemed irrelevant and therefore skipped! Title: {title}".format(
                                                                                        title=e.incident['title']
                                                                                    )
                    )
            continue
        except Exception as e:
            log.error("Couldn't scrape one of the incidents at {providerName}".format(
                                                                    providerName=e.providerModule.providerName
                                                                )
                     )
            continue
        data["incidents"].append(incident)

    return data
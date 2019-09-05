from lib.internals.tasks.verify import verify
# from lib.internals.tasks.extract import extract
# from lib.internals.tasks.scrape import scrape
# from lib.internals.tasks.sync import sync
# from lib.internals.tasks.notify import notify
# from lib.internals.tasks.prepare import prepare
# from lib.internals.tasks.cleanup import cleanup


# Verify all modular program parts (configurations, adapters, providers)
verify()

# # Extract all different procedures from the providers
# scrapingProcedures, preparationProcedures, cleanupProcedures = extract()

# # Scrape the needed data from the providers
# scrapedData = scrape(scrapingProcedures)

# # Synchronise the adapter with the scraped data
# events = sync(scrapedData)

# # Notify about the events which happened while syncronising
# notify(events)

# # Prepare for the next run through
# prepare(preparationProcedures)

# # Cleanup all which needes to be cleaned
# cleanup(cleanupProcedures)


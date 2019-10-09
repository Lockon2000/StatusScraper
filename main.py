from lib.internals.tasks.verify import verify
from lib.internals.tasks.extract import extract
from lib.internals.tasks.scrape import scrape
# from lib.internals.tasks.sync import sync
# from lib.internals.tasks.notify import notify
# from lib.internals.tasks.prepare import prepare
# from lib.internals.tasks.cleanup import cleanup


# Verify all modular program parts (configurations, adapters, providers)
verify()

# # Extract all different procedures from the providers
scrapingProcedures, preparationProcedures, cleanupProcedures = extract()

# # Scrape the needed data from the providers
data = scrape(scrapingProcedures)

# # Synchronise the adapter with the scraped data
# events = sync(data)

# # Notify about the events which where discovered while syncronising
# notify(events)

# # Prepare for the next program run through
# prepare(preparationProcedures)

# # Cleanup all which needes to be cleaned
# cleanup(cleanupProcedures)

from pprint import pprint
pprint(data)
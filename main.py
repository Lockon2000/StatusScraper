from lib.internals.tasks.start import start
from lib.internals.tasks.scrape import scrape
from lib.internals.tasks.crud import crud
from lib.internals.tasks.finish import finish


def main():
    # Make sure the ground work is set
    start()

    # Scrape the needed data from the providers
    data = scrape()

    # Synchronise the adapter
    crud(data)

    # Conclude any remaining work
    finish()


if __name__ == "__main__":
    # Run Application
    main()


from lib.internals.tasks.init import init
from lib.internals.tasks.crud import CRUD
from lib.internals.tasks.finish import finish

def main():
    # Make sure the ground work is set
    providers = init()

    # Actual porpuse of program
    CRUD(providers)

    # Conclude any remaining work
    finish()


if __name__ == "__main__":
    # Run Application
    main()


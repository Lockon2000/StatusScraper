from lib.utilities import *
from lib.init import init
from lib.objects.groups import CRUDGroups
from lib.objects.components import CRUDComponents
from lib.objects.incidents import CRUDIncidents
from lib.objects.maintenances import CRUDMaintenances


def main():
    init()

    CRUDGroups()
    CRUDComponents()
    CRUDIncidents()
    # CRUDMaintenances()      # Irrelevant for now!!


if __name__ == "__main__":
    # Run Application
    main()

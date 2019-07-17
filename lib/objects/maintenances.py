import json

import requests

from configs import dtadCachetAPI
from configs import APIKey
from enabledProviders import maintenanceFunctions
from lib.utilities.tools import log


# Global options
debug = False


# Main functionality
def CRUDMaintenances():
    for getMaintenances in maintenanceFunctions:
        for maintenance in getMaintenances():
            createMaintenance(maintenance)


# Helper functions
def createMaintenance(maintenance):
    payload = {}

    payload['name'] = maintenance['name']
    payload['message'] = maintenance['message']
    payload['scheduled_at'] = maintenance['scheduled_at']
    payload['completed_at'] = maintenance['completed_at']
    
    payload['status'] = 1

    try:
        response = requests.post("{}/schedules".format(dtadCachetAPI),
                                data=json.dumps(payload),
                                headers={'X-Cachet-Token': APIKey,
                                         'Content-Type': "application/json"})
        response.raise_for_status()
    except requests.HTTPError as e:
        log("Error", "Unsuccessful HTTP Request! Error Code {}".format(str(e)))
        log("Error", str(response.text))
    else:
        log("Success", "Created the maintenance {name} at the provider {providerName}".format(
                                                                                    name=maintenance['name'],
                                                                                    providerName=maintenance['provider']
                                                                                )
        )


if __name__ == "__main__":
    # Update Cachet maintenances database
    from pprint import pprint
    debug = True

    CRUDMaintenances()


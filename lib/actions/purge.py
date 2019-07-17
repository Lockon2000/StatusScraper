import json
from contextlib import closing

import requests

from configs import dtadCachetAPI, APIKey
from lib.utilities import *


def purg(endpoint):
    with closing(requests.get("{dtadCachetAPI}/{endpoint}".format(dtadCachetAPI=dtadCachetAPI, endpoint=endpoint))) as response:
        for endpointObject in response.json()['data']:
            try:
                response = requests.delete("{dtadCachetAPI}/{endpoint}/{id}".format(dtadCachetAPI=dtadCachetAPI, endpoint=endpoint, id=endpointObject['id']),
                                           headers={'X-Cachet-Token': APIKey})
                response.raise_for_status()
            except requests.HTTPError as e:
                log("Error", "Coulden't delete an object from the endpoint '{endpoint}/' !!!".format(endpoint=endpoint))
                log("Error", "Unsuccessful HTTP Request! Error Code {}".format(str(e)))

endpoints = ["components/groups", "components", "incidents", "schedules"]


if __name__ == '__main__':
    # Purge Cachet database
    for endpoint in endpoints:
        purg(endpoint)

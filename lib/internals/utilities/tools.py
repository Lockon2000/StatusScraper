from os import makedirs
from datetime import datetime
from locale import setlocale
from locale import LC_ALL
from contextlib import closing

from requests import get
from requests import HTTPError
from requests import Timeout
from requests import packages
from bs4 import BeautifulSoup

from conf.configs import logPath
from conf.configs import mainLogFile
from conf.configs import logLevel
from lib.internals.utilities.formatting import buildLogEntry


# Global options
packages.urllib3.disable_warnings()
setlocale(LC_ALL, "")
debug = False
makedirs(logPath, exist_ok=True)


def getThenParse(url, headers=None, cookies=None):
    parsedWebPage = None

    try:
        with closing(get(url, timeout=4, verify=False, headers=headers, cookies=cookies)) as response:
            parsedWebPage = BeautifulSoup(response.text, 'html.parser')
    except HTTPError as e:
        log("Error", "Unsuccessful HTTP Request for {url}. Error Code {code}".format(url=url, code=e))
        raise e
    except Timeout as e:
        log("Error", "Request timed out for {url}".format(url=url))
    except Exception as e:
        log("Error", "Request for {url} failed!".format(url=url))
        raise e

    return parsedWebPage

def log(logType, message):
    dateFormat = "%a %x %X"
    date = datetime.now().strftime(dateFormat)

# Case differentiation if needed
# if logType == "Info":
# elif logType == "Success":
# elif logType == "Error":
# else:
    with open(mainLogFile, "a") as file:
        file.write(buildLogEntry(date, logType, message))

# must be revised
def moduleSyntaxCorrect(module):
    try:
        module.providerName
    except AttributeError:
        return False

    return True


if __name__ == '__main__':
    # Test module
    from pprint import pprint
    debug = True

    pprint("No Tests yet!")

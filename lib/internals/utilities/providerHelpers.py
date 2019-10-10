from locale import setlocale
from locale import LC_ALL
from contextlib import closing

from requests import get
from requests import packages

from bs4 import BeautifulSoup


# Global options
packages.urllib3.disable_warnings()     # Disable all SSL/TLS certificate warnings
setlocale(LC_ALL, "")                   # (((((Don't remember why we need this)))))


def getWebpageThenParse(url, headers=None, cookies=None):
    parsedWebPage = None

    with closing(get(url, timeout=4, verify=False, headers=headers, cookies=cookies)) as response:
        parsedWebPage = BeautifulSoup(response.text, 'html.parser')

    return parsedWebPage


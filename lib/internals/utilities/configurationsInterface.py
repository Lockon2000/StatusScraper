import os
import logging

from lib.internals.structures.classes import CaseInsensitiveDict
from conf.configs import *      # You do not need to worry about syntax errors, verifyConfigurations guarantees it.

# Process the configurations

# adapter
adapter = adapter.lower()

# APIBaseURL
if APIBaseURL.endswith("/"):
    # Remove the end slash
    APIBaseURL = APIBaseURL[:-1]
# Lower case
APIBaseURL = APIBaseURL.lower()

# APIKey
APIKey = APIKey

# logPath
if not logPath.endswith("/"):
    # Add the end slash
    logPath = logPath + "/"
# Resolve path
logPath = os.path.abspath(logPath)

# logFiles
logFiles = [
    # Convert the severity to the enum values of the logging module
    (name, {
        "debug":    logging.DEBUG,
        "info":     logging.INFO,
        "warning":  logging.WARNING,
        "error":    logging.ERROR,
        "critical": logging.CRITICAL
    }[severity]) 
    for name, severity in logFiles
]

# enabledProviders
enabledProviders = [
    name.lower()
    for name in enabledProviders
]

# manualComponents
manualComponents = [
    (provider.lower(), component.lower())
    for provider, component in manualComponents
]

# The existence of "conf/blacklist.py" is not guaranteed
if os.path.isfile("conf/blacklist.py"):
    from conf.blacklist import *    # You do not need to worry about syntax errors, verifyConfigurations guarantees it.

    # componentsBlacklist (Not guaranteed existence)
    if "componentsBlacklist" in locals():
        componentsBlacklist = CaseInsensitiveDict(componentsBlacklist)

    # incidentsBlacklist (Not guaranteed existence)
    if "incidentsBlacklist" in locals():
        incidentsBlacklist = CaseInsensitiveDict(incidentsBlacklist)
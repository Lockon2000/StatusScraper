from os import path
import logging

from lib.internals.utilities.configurationsInterface import logPath
from lib.internals.utilities.configurationsInterface import logFiles


# Global Settings:
logFormat = "%(levelname)s - %(asctime)s - %(message)s"
dateFormat = "%d-%m-%y %H:%M:%S"


# Logger Definition:

# Create the logger
logger = logging.getLogger(__name__)
# Set the logger severity level (logging.DEBUG in order to consider everything and filter at the handler level)
logger.setLevel(logging.DEBUG)

# For every configured log file create a handler with the configured severity level
for logFile in logFiles:
    # Consult configurationsInterface.md for more info about the `logFiles` variable.
    logHandler = logging.FileHandler(path.join(logPath, logFile[0]))
    logLevel = logFile[1]
    logHandler.setLevel(logLevel)
    logFormatter = logging.Formatter(fmt=logFormat, datefmt=dateFormat)
    logHandler.setFormatter(logFormatter)

    logger.addHandler(logHandler)


# Interface:
log = logger

log.debug("Advanced logging has been established")


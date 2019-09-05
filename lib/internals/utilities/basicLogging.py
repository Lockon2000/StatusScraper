from os import path
import logging


# Global Settings:
logFormat = "%(levelname)s - %(asctime)s - %(message)s"
dateFormat = "%d-%m-%y %H:%M:%S"


# Logger Definition:

# Create the logger
logger = logging.getLogger(__name__)
# Set the logger severity level (logging.ERROR as the basic logger is only needed for logging errors and critical
# events up to the point were advanced logging can be established).
logger.setLevel(logging.ERROR)

# Create one handler for the output.log file in ./logs
logHandler = logging.FileHandler("./logs/output.log")
logLevel = logging.ERROR
logHandler.setLevel(logLevel)
logFormatter = logging.Formatter(fmt=logFormat, datefmt=dateFormat)
logHandler.setFormatter(logFormatter)

logger.addHandler(logHandler)


# Interface:
log = logger


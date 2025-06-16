#!/usr/bin/env python3
"""Handles all logging code :)"""

import logging
from .files import LOG_FILE

LOGGING_FORMAT = "%(asctime)s [%(levelname)s]: \"%(message)s\""  # ? The format for the logging msg
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # ? The format for the date in the logging message

logger = logging.getLogger(__name__)  # Get the logger
formatter = logging.Formatter(fmt=LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)  # Set the formatter
fileHandler = logging.FileHandler(LOG_FILE, encoding="UTF-8")  # Set up file handler, were using write mode here so it overwrites the file if it already exists
fileHandler.setFormatter(formatter)  # Add the formatter
logger.addHandler(fileHandler)  # Add it to logger

# ! ONLY FOR DEBUG PURPOSES
if __debug__:
    consoleHandler = logging.StreamHandler()  # Set up stream handler
    consoleHandler.setFormatter(formatter)  # Apply the formatter
    logger.addHandler(consoleHandler)  # Add the handler
    logger.level = logging.DEBUG  # Set level to debug
else:
    logger.level = logging.INFO  # Set level to info

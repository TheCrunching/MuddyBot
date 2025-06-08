#!/usr/bin/env python3
"""Handles all logging code :)"""

import logging
from .files import LOG_FILE

LOGGING_FORMAT = "[%(asctime)s] %(levelname)s: \"%(message)s\""
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger(__name__)# Set up logger object
formatter = logging.Formatter(fmt=LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)# Set up formatter
fileHandler = logging.FileHandler(LOG_FILE, encoding="UTF-8", mode="w")# Set up file handler
fileHandler.setFormatter(formatter)# Add the formatter
logger.addHandler(fileHandler)# Add it to logger
if __debug__:
    consoleHandler = logging.StreamHandler()# Set up stream handler
    consoleHandler.setFormatter(formatter)# Apply the formatter
    logger.addHandler(consoleHandler)# Add the handler
    logger.level = logging.DEBUG
else:
    logger.level = logging.INFO

#!/usr/bin/env python3
"""Python twitch bot."""

# Standard library imports
from tomllib import load as tload

# Local imports
from .files import CONFIG_FILE
from .twitch_bot import TwitchBot
from .logger import logger

__version__ = "1.1.0-rc1"


def main() -> int:
    """This is just the main function :) It handles reading the config file"""

    try:
        with open(CONFIG_FILE, "rb") as fp:  # Open the config file
            config = tload(fp)  # Load the TOML
            try:
                try:  # Next we try to get each value out of the config file and see if we fail
                    token = config['token']
                    if not isinstance(token, str):
                        raise TypeError("The 'token' field must be a string.")
                except KeyError:
                    logger.error("OAUTH token not set.")
                    return 1  # Exit with code 1
                try:
                    channel = config['channel']
                    if not isinstance(channel, list):
                        logger.critical("channel must be list.")
                        raise TypeError("The 'channel' field must be a list.")
                    logger.debug(channel)
                except KeyError:
                    logger.error("Channel must be set in the config file.")
                    return 1  # Exit with code 1
                try:
                    key = config['key']
                    if not isinstance(key, str):
                        raise TypeError("The 'key' field must be a string.")
                except KeyError:
                    logger.critical("Encryption key not found in the config file.")
                    return 1  # Exit with code 1
            except TypeError as error_message:
                logger.error(error_message)
                return 1  # Return exit code of 1
    except FileNotFoundError:  # If the config file was not found we fail
        logger.critical("Config file: '%s' not found.", CONFIG_FILE)
        return 1  # Return with exit code 1

    bot = TwitchBot(token, channel, key)  # If we did'nt fail at all we run the twitch bot
    bot.run()  # Run it

    return 0  # ? Our installer script will handle exiting.

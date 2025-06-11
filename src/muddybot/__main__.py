#!/usr/bin/env python3
"""Python twitch bot."""

# Standard library imports
from tomllib import load as tload
from argparse import ArgumentParser

# Local imports
from .files import CONFIG_FILE
from .twitch_bot import TwitchBot
from .logger import logger

__version__ = "1.0.1+snapshot25w25a"

parser = ArgumentParser(
    prog="MuddyBot",
    description="A twitch bot for Mud Flaps (twitch.tv/mud_flaps123)",
    epilog="..."
)
parser.add_argument(
    "-v",
    action="version",
    version=__version__,
    help="Displays the programs version :)"
)
args = parser.parse_args()# Parse the args

def main() -> int:
    """This is just the main function :)"""
    try:
        with open(CONFIG_FILE, "rb") as fp:
            config = tload(fp)
            try:
                token = config['token']
            except KeyError:
                logger.error("OAUTH token not set.")
                print("OAUTH token not set.")
                return 1# Exit with code 1
            try:
                channel = config['channel']
                logger.debug(channel)
            except KeyError:
                logger.error("Channel must be set.")
                print("You must set the channel in the config file.")
                return 1# Exit with code 1
            try:
                key = config['key']
            except KeyError:
                logger.critical("Encryption key not found :(")
                print("Set the 'key' field in your config file to your encryption key")
                return 1# Exit with code 1
    except FileNotFoundError:
        logger.critical("Config file: '%s' not found.", CONFIG_FILE)
        print(f"Config file: '{CONFIG_FILE}' not found.")
        return 1# Return with exit code 1

    bot = TwitchBot(token, channel, key)
    bot.run()

    return 0# ? Our installer script will handle exiting.

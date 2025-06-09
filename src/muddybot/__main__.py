#!/usr/bin/env python3
"""Python twitch bot."""

# Standard library imports
import sys
import tomllib
from argparse import ArgumentParser

# Local imports
from .files import CONFIG_FILE
from .twitch_bot import TwitchBot
from .logger import logger

__version__ = "1.0.0+pre2"

parser = ArgumentParser(
    prog="MuddyBot",
    description="A twitch bot for Mud Flaps (twitch.tv/mud_flaps123)",
    epilog="..."
)
parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=__version__,
    help="Displays the programs version :)"
)
args = parser.parse_args()# Parse the args

def main():
    """This is just the main function :)"""
    try:
        with open(CONFIG_FILE, "rb") as fp:
            config = tomllib.load(fp)
            try:
                token = config['token']
            except KeyError:
                logger.error("OAUTH token not set.")
                print("OAUTH token not set.")
                sys.exit(1)
            try:
                channel = config['channel']
                logger.debug(channel)
            except KeyError:
                logger.error("Channel must be set.")
                print("You must set the channel in the config file.")
                sys.exit(1)
            try:
                key = config['key']
            except KeyError:
                logger.critical("Encryption key not found :(")
                print("Set the 'key' field in your config file to your encryption key")
                sys.exit(1)
    except FileNotFoundError:
        logger.critical("Config file: '%s' not found.", CONFIG_FILE)
        print(f"Config file: '{CONFIG_FILE}' not found.")
        sys.exit(1)

    bot = TwitchBot(token, channel, key)
    bot.run()

    return 0# ? Are installer script will handle exiting.

if __name__ == "__main__":
    main()

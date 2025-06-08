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

__version__ = "0.1.3+snapshot25w24a"

parser = ArgumentParser(
    prog="Twitch bot",
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
logger.debug("Parsed the command line arguments: '%s'", args)# Log them

    @commands.command()
    async def start_word(self, ctx: commands.Context):
        if ctx.author.is_mod or ctx.author.is_broadcaster:
            if self.word is None:
                logger.error("Can't start words on stream cause word is None")
                await ctx.reply("Error, can't start words on stream cause word is not set :(")
                return
            self.search_word = True
            await ctx.reply(f"{ctx.author.name} started words on stream")
        else:
            await ctx.reply(f"{ctx.author.name} you can't do that :(")

    @commands.command()
    async def stop_word(self, ctx: commands.Context):
        if ctx.author.is_mod or ctx.author.is_broadcaster:
            self.search_word = False
            await ctx.reply(f"{ctx.author.name} stopped words on stream")
        else:
            await ctx.reply(f"{ctx.author.name} you can't do that :(")

    @commands.command()
    async def send_love(self, ctx: commands.Context, person: str):
        await ctx.send(f"{ctx.author.name} is sending {person} a whole lot of love <3")

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

    try:
        bot = TwitchBot(token, channel, key)
        bot.run()
    except KeyboardInterrupt:
        print("Ctrl+c pressed, exiting...")
        sys.exit()

if __name__ == "__main__":
    main()

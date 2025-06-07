#!/usr/bin/env python3

"""Python twitch bot."""

from pathlib import Path
from os import mkdir
from datetime import datetime
from json import load, dump
from argparse import ArgumentParser
import logging
from twitchio.ext import commands

__version__ = "0.1.1+snapshot25w23a"
__data_dir__ = Path(Path.home(), ".twbot/")
if not Path(__data_dir__).exists():
    mkdir(Path(Path.home()))

__log_file__ = Path(__data_dir__, "log.txt")

loggingFormat = "[%(asctime)s] %(levelname)s: \"%(message)s\""
loggingDateFormat = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger(__name__)# Set up logger object
formatter = logging.Formatter(fmt=loggingFormat, datefmt=loggingDateFormat)# Set up formatter object
fileHandler = logging.FileHandler(__log_file__)# Set up file handler
fileHandler.setFormatter(formatter)# Add the formatter
logger.addHandler(fileHandler)# Add it to logger
if __debug__:
    consoleHandler = logging.StreamHandler()# Set up stream handler
    consoleHandler.setFormatter(formatter)# Apply the formatter
    logger.addHandler(consoleHandler)# Add the handler
    logger.level = logging.DEBUG
else:
    logger.level = logging.INFO

time = datetime.now()

logger.info(f"We are online at: \"{time}\"")

parser = ArgumentParser(prog="Twitch bot", description="A twitch bot for Mud Flaps (twitch.tv/mud_flaps123)", epilog="...")
parser.add_argument("-v", "--version", action="version", version=__version__, help="Displays the programs version :)")
parser.add_argument("-a", "--add", help="Not implemented.")
args = parser.parse_args()
logger.debug(f"Parsed the command line arguments: \"{args}\"")

class Bot(commands.Bot):
    def __init__(self, token, word):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.word = word
        super().__init__(token=token, prefix=['c!', "!"], initial_channels=['mud_flaps123'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        logger.debug(f"Logged in as \"{self.nick}\" with id \"{self.user_id}\"")
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        logger.debug(f"{message.author.name}: {message.content}")
        for a in message.content.split(" "):
            print(a)
            logger.debug(f"Word: {a}")
            if a.lower() == self.word.lower():
                print(f"{message.author.name} correctly guessed: \"{self.word}\"")

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')# Cool hello command

    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.send("Commands: c!hello, c!help, c!online, !unlurk, !wordsOnStream")# Help command

    @commands.command()
    async def online(self, ctx: commands.Context):
        await ctx.send(f"Online since: {time}. Which is {datetime.now()-time} amount of uptime :)")

    @commands.command()
    async def unlurk(self, ctx: commands.Context):
        await ctx.reply(f"{ctx.author.name} has unlurked themselves :)")

    @commands.command()
    async def song(self, ctx: commands.Context):
        await ctx.reply(f"Turns out the !song command does not work :(")

    @commands.command()
    async def wordsOnStream(self, ctx: commands.Context):
        await ctx.reply("Words on stream is what we do every 30 minutes where the chatters try to guess a word! Guess the word spin the wheel!")

    @commands.command()
    async def boop(self, ctx: commands.Context):
        await ctx.reply(f"{ctx.author.name} was booped! HAHAHA.")

def main():
    config_file = Path(__data_dir__, "config.json")
    if not config_file.exists():
        with open(config_file, "w", encoding="UTF-8") as fp:
            dump({"token": "SET_TOKEN"}, fp, indent=4)
        print(f"Set 'token' to your twitch OAUTH token in {config_file}")
    else:
        with open(config_file, "r", encoding="UTF=8") as fp:
            config = load(fp)
        try:
            word = config['word']
        except KeyError:
            word = "                                                                               "
        logger.debug(f"Word is: \"{word}\"")
        bot = Bot(config['token'], word)
        bot.run()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

"""Python twitch bot."""

# Standard library imports
import sys
import logging
import tomllib
from os import mkdir
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser

# Twitch API module import
from twitchio.ext import commands

__version__ = "0.1.2+snapshot25w23b"
__data_dir__ = Path(Path.home(), ".twbot/")
if not Path(__data_dir__).exists():
    mkdir(Path(Path.home()))

__log_file__ = Path(__data_dir__, "twbot.log")
try:
    __log_file__.unlink()# Delete the log file.
except FileNotFoundError:
    pass# We don't care if it's not their since we were deleting it anyway

__command_file__ = Path(__data_dir__, "commands.json")# The file to store commands in

LOGGING_FORMAT = "[%(asctime)s] %(levelname)s: \"%(message)s\""
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger(__name__)# Set up logger object
formatter = logging.Formatter(fmt=LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)# Set up formatter
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

# Set up logger for twitch chat
chatLogger = logging.getLogger(__name__)
chatFileHandler = logging.FileHandler(Path(__data_dir__, f"chat-{datetime.today().strftime('%Y-%m-%d')}.log"))
chatFileHandler.setFormatter(logging.Formatter(fmt="[%(asctime)s] %(message)s", datefmt=LOGGING_DATE_FORMAT))
chatLogger.addHandler(chatFileHandler)
chatLogger.level = logging.INFO

parser = ArgumentParser(
    prog="Twitch bot",
    description="A twitch bot for Mud Flaps (twitch.tv/mud_flaps123)",
    epilog="..."
)
parser.add_argument("-v", "--version", action="version", version=__version__, help="Displays the programs version :)")
args = parser.parse_args()# Parse the args
logger.debug(f"Parsed the command line arguments: '{args}'")# Log them


time = datetime.now()

logger.info(f"We are online at: '{time}'")

class Bot(commands.Bot):
    def __init__(self, token, word, channel):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.word = word
        self.search_word = False
        super().__init__(token=token, prefix=['c!', "!"], initial_channels=channel)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        logger.debug(f"Logged in as '{self.nick}' with id '{self.user_id}'")
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            logger.debug(f"Bot sent: {message.content}")
            chatLogger.info(f"notmud_flaps123: {message.content}")
            return

        # Print the contents of our message to console...
        chatLogger.info(f"{message.author.name}: {message.content}")
        logger.debug(f"{message.author.name}: {message.content}")
        if (self.word is not None) and (self.search_word):
            for a in message.content.split(" "):
                print(a)
                logger.debug(f"Word: {a}")
                if a.lower() == self.word.lower():
                    print(f"{message.author.name} correctly guessed: '{self.word}'")

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')# Cool hello command

    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.send("Commands: c!hello, c!help, c!online, !unlurk, !wordsOnStream, !send_love <person>. Moderator only: c!start_word, c!stop_word")# Help command

    @commands.command()
    async def online(self, ctx: commands.Context):
        await ctx.send(f"Online since: {time}. Which is {datetime.now()-time} amount of uptime :)")

    @commands.command()
    async def unlurk(self, ctx: commands.Context):
        await ctx.send(f"{ctx.author.name} has unlurked themselves :)")

    @commands.command()
    async def song(self, ctx: commands.Context):
        await ctx.reply(f"Turns out the !song command does not work :(")

    @commands.command()
    async def wordsOnStream(self, ctx: commands.Context):
        await ctx.reply("Words on stream is what we do every 30 minutes where the chatters try to guess a word! Guess the word spin the wheel!")

    @commands.command()
    async def boop(self, ctx: commands.Context):
        await ctx.reply(f"{ctx.author.name} was booped! HAHAHA.")

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
    config_file = Path(__data_dir__, "config.toml")
    try:
        with open(config_file, "rb") as fp:
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
                word = config['word']
                logger.debug(word)
            except KeyError:
                logging.info("Word not in config file. Defaulting to 'None'")
                word = None
    except FileNotFoundError:
        logger.critical(f"Config file: '{config_file}' not found.")
        print(f"Config file: '{config_file}' not found.")
        sys.exit(1)

    try:
        bot = Bot(token, word, channel)
        bot.run()
    except KeyboardInterrupt:
        print("Ctrl+c pressed, exiting...")
        sys.exit()

if __name__ == "__main__":
    main()

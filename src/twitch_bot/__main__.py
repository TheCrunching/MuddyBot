#!/usr/bin/env python3

"""Python twitch bot."""

from pathlib import Path
from os import mkdir
from datetime import datetime
import logging
import json
from twitchio.ext import commands

__version__ = "0.1.0"
__log_file__ = Path(Path.home(), ".twbot/log.txt")
time = datetime.now()

loggingFormat = "[%(asctime)s] %(levelname)s: \"%(message)s\""
loggingDateFormat = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger(__name__)# Set up logger object
formatter = logging.Formatter(fmt=loggingFormat, datefmt=loggingDateFormat)# Set up formatter object
fileHandler = logging.FileHandler(__log_file__)# Set up file handler
fileHandler.setFormatter(formatter)# Add the formatter
logger.addHandler(fileHandler)# Add it to logger
if __debug__:
    consoleHandler =logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addFilter(consoleHandler)

logger.level = logging.DEBUG

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
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        logger.debug(f"{message.author.name}: {message.content}")
        if message.content.lower() == self.word.lower():
            print(f"{message.author.name} correctlly guessed: \"{self.word}\"")

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
        await ctx.reply(f"Words on stream is what we do every 30 minutes where the chatters try to guess a word! Guess the word spin the wheel!")

def main():
    config_file = Path(Path.home(), ".twbot/config.json")
    if not config_file.exists():
        if not Path(Path.home(), ".twbot/").exists():
            mkdir(Path(Path.home(), ".twbot/"))
        with open(config_file, "w", encoding="UTF-8") as fp:
            json.dump("{\"token\": SET_TOKEN}", fp)
        print(f"Set 'token' to your twitch OAUTH token in {config_file}")
    else:
        with open(config_file, "r", encoding="UTF=8") as fp:
            config = json.load(fp)
        try:
            word = config['word']
        except KeyError:
            word = "                                                                                         "
        bot = Bot(config['token'], word)
        bot.run()

if __name__ == "__main__":
    main()

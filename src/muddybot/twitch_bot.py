#!/usr/bin/env python3
"""Twitch bot code"""

from datetime import datetime
import logging

# Twitch API module import
from twitchio.ext import commands

# Crypto module
from cryptography.fernet import Fernet, InvalidToken

from .files import CHAT_LOG_FILE
from .logger import logger, LOGGING_DATE_FORMAT

# Set up logger for twitch chat
chatLogger = logging.getLogger(__name__)
chatFileHandler = logging.FileHandler(CHAT_LOG_FILE, encoding="UTF-8", mode="a")
chatFileHandler.setFormatter(
    logging.Formatter(
        fmt="[%(asctime)s] %(message)s",
        datefmt=LOGGING_DATE_FORMAT
    )
)
chatLogger.addHandler(chatFileHandler)
chatLogger.level = logging.INFO

class TwitchBot(commands.Bot):
    """This is are twitch bot!
    """
    def __init__(self, token, channel, key):
        self.word = None# Set the word as None cause we have not set it yet.
        self.search_word = False# We don't want to start off by searching for the word.

        self.time = datetime.now()
        self.key = key
        logger.info("We are online at: '%s'", self.time)

        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=token, prefix=['c!', "!"], initial_channels=channel)

    async def event_ready(self):
        """Called when bot is ready
        """
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        logger.debug("Logged in as '%s' with id '%s'", self.nick, self.user_id)
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        """Called when a message is sent in twitch chat

        Args:
            message (_type_): The message object that was sent
        """

        if message.echo:# Messages with echo set to True are messages sent by the bot
            chatLogger.info("%s: %s", self.nick, message.content)
            return

        # Print the contents of our message to console...
        chatLogger.info("%s: '%s'", message.author.name, message.content)
        logger.debug("%s: %s", message.author.name, message.content)
        if (self.word is not None) and (self.search_word):
            for a in message.content.split(" "):
                print(a)
                logger.debug("Word: %s", a)
                if a.lower() == self.word.lower():
                    await self.connected_channels[0].send(
                        f"{message.author.name} correctly guessed: '{self.word}'"
                    )
                    self.search_word = False
        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        """This implements the c!hello/!hello command
        """

        await ctx.send(f'Hello {ctx.author.name}!')# Cool hello command

    @commands.command()
    async def help(self, ctx: commands.Context):
        """Implements the c!help/!help command, help messages are a must have.
        """

        await ctx.send("Commands: c!hello, c!help, c!status, !unlurk, !send_love <person>, c!mud_curses. Moderator only: c!start_word, c!stop_word, Admin only: c!set_word <word> (encrypted ofc)")# Help command

    @commands.command()
    async def status(self, ctx: commands.Context):
        """Implements the c!status/!status command
        """

        await ctx.send(f"Online since: {self.time}. Which is {datetime.now()-self.time} amount of uptime :)")

    @commands.command()
    async def unlurk(self, ctx: commands.Context):
        """Implements the c!unlurk/!unlurk command, honestly why was'nt this a thing?
        """

        await ctx.send(f"{ctx.author.name} has unlurked themselves :)")

    @commands.command()
    async def song(self, ctx: commands.Context):
        """Implements the c!song/!song command. When the command fails we gotta tell the user right?
        """

        await ctx.reply("Turns out the !song command does not work :(")

    @commands.command()
    async def start_word(self, ctx: commands.Context):
        """Implements the c!start_word/!start_word command, this is the main purpose of this bot and is why I made it.
        """

        if ctx.author.is_mod or ctx.author.is_broadcaster or ((ctx.author.name == "thecrunching123") and __debug__):
            if self.word is None:
                logger.error("Can't start words on stream cause word is None")
                await ctx.reply("Error, can't start words on stream cause word is not set :(")
                return
            
            if self.search_word:
                await ctx.reply("Words on stream already started so can't stop.")
            else:
                self.search_word = True
                await ctx.reply(f"{ctx.author.name} started words on stream")
        else:
            await ctx.reply(f"{ctx.author.name} you can't do that :(")

    @commands.command()
    async def stop_word(self, ctx: commands.Context):
        """Implements the c!stop_word/!stop_word command, this is the main purpose of this bot and is why I made it.
        """

        if ctx.author.is_mod or ctx.author.is_broadcaster or ((ctx.author.name == "thecrunching123") and __debug__):
            if self.search_word:
                self.search_word = False
                await ctx.reply(f"{ctx.author.name} stopped words on stream")
            else:
                await ctx.reply("Words on stream was already stopped")
        else:
            await ctx.reply(f"{ctx.author.name} you can't do that :(")

    @commands.command()
    async def send_love(self, ctx: commands.Context, person: str = "Everyone"):
        """Implements c!send_love/!send_love. "I just wanna use your love tonight"
        """

        await ctx.send(f"{ctx.author.name} is sending {person} a whole lot of love <3")

    @commands.command()
    async def mud_curses(self, ctx: commands.Context):
        """Implements c!mudcurses/!mudcurses. Historic occasion.
        """

        await ctx.send("This is the clip where Mud cursed :) https://www.twitch.tv/mud_flaps123/clip/SuccessfulFineMarjoramAMPTropPunch-OYgRM7gAVs1L3H-q clipped by: https://www.twitch.tv/chunckly")

    @commands.command()
    async def set_word(self, ctx: commands.Context, word: str = None):
        """Get word into the program"""

        if ctx.author.is_broadcaster or ((ctx.author.name == "thecrunching123") and __debug__):# Will only let crunching do admin commands if __debug__ is true
            if word is not None:
                try:
                    self.word = await decrypt(word, self.key)
                except InvalidToken:
                    await ctx.reply("Invalid text :) try again.")
                    return None
                await ctx.send(f"{ctx.author.name} set the word for words on stream :)")
                logger.debug(self.word)
            else:
                logger.warning("User tried to set word without specify text.")
                await ctx.reply("RIP you failed forgot to add the text to the command :(")
        else:
            ctx.reply(f"{ctx.author.name} you do not have permission for that :(")

async def decrypt(text, key) -> str:
    """Decrypts the message

    Args:
        text (_type_): The text
        key (_type_): The encryption key

    Returns:
        str: The decrypted text
    """

    return Fernet(key).decrypt(text).decode()

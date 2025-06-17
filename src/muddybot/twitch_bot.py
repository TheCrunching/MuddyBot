#!/usr/bin/env python3
"""Twitch bot code"""

import re
import logging
from datetime import datetime, timezone

# Twitch API module import
from twitchio.ext import commands

# Crypto module
from cryptography.fernet import Fernet, InvalidToken

from emoji import demojize

from .words import word_list
from .files import get_chat_log_file
from .logger import logger, LOGGING_DATE_FORMAT


class TwitchBot(commands.Bot):
    """This is are twitch bot!"""
    def __init__(self, token, channel, key):
        self.word = None  # Set the word as None cause we have not set it yet.
        self.search_word = False  # We don't want to start off by searching for the word.

        self.time = datetime.now(timezone.utc)
        self.key = key
        logger.info("We are online at: '%s'", self.time)

        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=token, prefix=['c!', "m!", "!"], initial_channels=channel)

    def set_up_log_file(self):
        """Generates the file handler

        Returns:
            The file handler
        """

        self.chat_log_file = get_chat_log_file()
        chat_file_handler = logging.FileHandler(self.chat_log_file, encoding="UTF-8")
        chat_file_handler.setFormatter(
            logging.Formatter(
                fmt="[%(asctime)s] %(message)s",
                datefmt=LOGGING_DATE_FORMAT
            )
        )

        self.chatLogger.addHandler(chat_file_handler)

    async def event_ready(self):
        """Called when bot is ready"""
        logger.debug(self.connected_channels)
        logger.debug("Logged in as '%s' with id '%s'", self.nick, self.user_id)

        self.chatLogger = logging.getLogger(__name__)

        self.set_up_log_file()
        self.chatLogger.level = logging.INFO

    async def event_message(self, message):
        """Called when a message is sent in twitch chat"""
        if self.chat_log_file != get_chat_log_file():
            self.chatLogger.removeHandler(self.chatLogger.handlers[0])
            self.set_up_log_file()
        if message.echo:  # Messages with echo set to True are messages sent by the bot
            logger.debug("%s: %s", self.nick, message.content)
            self.chatLogger.info("%s: %s", self.nick, demojize(message.content))

            return

        self.chatLogger.info("%s: '%s'", message.author.name, demojize(message.content))
        logger.debug("%s: %s", message.author.name, message.content)
        if (self.word is not None) and (self.search_word):
            for a in message.content.split(" "):
                logger.debug("Word: %s", a)
                if a.lower() == self.word.lower():
                    await message.channel.send(
                        f"{message.author.mention} correctly guessed: '{self.word}"
                    )
                    self.search_word = False

        # Check if user is saying Historic
        if message.first:
            logger.debug("User %s just typed their first message which is %s", message.author.name, message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def help(self, ctx: commands.Context):
        """Implements the c!help/!help command, help messages are a must have."""

        await ctx.send("Commands: c!help, c!status, !unlurk, c!find_matches <word>. Moderator only: c!start_word, c!stop_word, Admin only: c!set_word <word> (encrypted ofc)")# Help command

    @commands.command()
    async def status(self, ctx: commands.Context):
        """Implements the c!status/!status command"""

        await ctx.send(
            f"Online since: {self.time} which is {datetime.now(timezone.utc)-self.time} amount of uptime :)"
        )

    @commands.command()
    async def start_word(self, ctx: commands.Context):
        """Implements the c!start_word/!start_word command, this is the main purpose of this bot and is why I made it."""

        if ctx.author.is_mod or ctx.author.is_broadcaster or ((ctx.author.name == "thecrunching123") and __debug__):
            if self.word is None:
                logger.error("Can't start words on stream cause word is None")
                await ctx.reply("Error, can't start words on stream cause word is not set :(")
                return

            if self.search_word:
                await ctx.reply("Words on stream already started so can't stop.")
            else:
                self.search_word = True
                await ctx.reply(f"{ctx.author.mention} started words on stream")
        else:
            await ctx.reply(f"{ctx.author.mention} you can't do that :(")

    @commands.command()
    async def stop_word(self, ctx: commands.Context):
        """Implements the c!stop_word/!stop_word command, this is the main purpose of this bot and is why I made it."""

        if ctx.author.is_mod or ctx.author.is_broadcaster or ((ctx.author.name == "thecrunching123") and __debug__):
            if self.search_word:
                self.search_word = False
                await ctx.reply(f"{ctx.author.mention} stopped words on stream")
            else:
                await ctx.reply("Words on stream was already stopped")
        else:
            await ctx.reply(f"{ctx.author.mention} you can't do that :(")

    @commands.command()
    async def set_word(self, ctx: commands.Context, word: str = None):
        """Get word into the program"""

        if ctx.author.is_broadcaster or ((ctx.author.name == "thecrunching123") and __debug__):# Will only let crunching do admin commands if __debug__ is true
            if word is not None:
                try:
                    self.word = await self.decrypt(word, self.key)
                    self.word = self.word.lower()
                except InvalidToken:
                    await ctx.reply("Invalid text :) try again.")
                    return None
                if await self.getMatches(self.word) > 0:
                    await ctx.send(f"{ctx.author.mention} set the word for words on stream :)")
                else:
                    await ctx.send(f"{ctx.author.mention} their are no matches for the word you set. Set the word anyway.")
                logger.debug(self.word)
            else:
                logger.warning("User tried to set word without specify text.")
                await ctx.reply("RIP you failed forgot to add the text to the command :(")
        else:
            await ctx.reply(f"{ctx.author.mention} you do not have permission for that :(")

    @commands.command()
    async def find_matches(self, ctx: commands.Context, word: str = None):
        """Implements the c!find_matches command"""
        if word is None:
            await ctx.reply("You must pass a string to match, eg __pl_")
        else:
            await ctx.send(f"Found '{await self.getMatches(word)}' matches for {word}.")

    async def decrypt(self, text: str, key: str) -> str:
        """Decrypts the message

        Args:
            text (str): The text
            key (str): The encryption key

        Returns:
            str: The decrypted text
        """

        return Fernet(key).decrypt(text).decode()

    async def get_matches(self, pattern: str) -> int:
        """_summary_

        Args:
            pattern (str): The word pattern

        Returns:
            int: How many words were found
        """
        # Replace underscores with regex pattern for any character
        regex_pattern = pattern.replace('_', '.')

        # Compile the regex pattern
        regex = re.compile(f'^{regex_pattern}$')

        # Find matches
        matches = [word for word in word_list if regex.match(word)]

        return len(matches)

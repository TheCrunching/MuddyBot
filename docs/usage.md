# Usage

This document describes how to use MuddyBot.

## Installing

To install download the ***.whl*** file for the latest version. After than run `pip install .fileyoudownloaded`. Now you can run the program as `muddybot`.

But before you do that we need to set some config stuff up.

## Configuration

The configuration for MuddyBot is stored in ***~/.muddybot/muddy_config.toml***.

The configuration file should look like this:

```toml
token = "YOUR TWITCH BOT TOKEN"
channel = ["Your channel"]# Can be a list of channels to listen to
key = "YOUR ENCRYPTION KEY"
```

If you are running in non debug mode set the "PYTHONOPTIMIZE" environment variable to 1 eg `export PYTHONOPTIMIZE=1`.

### Token

You can get a token using this website [Twitch Token Generator](https://twitchtokengenerator.com/). You must keep this a secret. If you share other people will be able to use your bot.

### Channel

The channel field is a list of channels the bot should listen to. Their must be at least one channel in the list though.

### Key

The key field holds the encryption key for securlly getting the word to the bot from twitch chat. You can get your own key by running `muddybot-key`, after that put the value it printed to the terminal in your config file.

## Commands

This section describes the available commands for the twitch bot.

All commands can be called `c!command` or `!command` it is up to the user to decide on which to use.

### c!hello

This command can be run by anyone and return **Hello {user}!**.

### c!help

This command prints a help message of available commands.

### c!status

This commands prints the uptime of the program.

### c!unlurk

This command unlurks the user. I was always annoyed their was never a unlurk command in [Mud Flaps twitch chat](https://twitch.tv/mud_flaps123), so I made one.

### c!song

This command alerts the user that the `!song` command does not work.

### c!start_word and c!stop_word

c!start_word and c!stop_word start and stop words on stream respectfully. These commands can only be run by the broadcaster or a moderator. See [Words on stream](#words-on-stream).

### c!send_love person

This command sends love's to the specified person.

### c!mud_curses

Prints a url to the clip where Mud Flaps cursed. Cause why not?

### c!set_word word

Sets the word for words on stream. The word must be encrypted with the same encryption key the program is using.

## Words on stream

Words on stream is something Mud Flaps does in his stream. Every 30 minutes he reveals a letter and his chat has to guess the word. This bot was made to help with that and find the word. You use `c!start_word` to start words on stream and `c!stop_word` to stop words on stream. If the user correctly guess's the word the bot will alert the user that they guessed it correctly and stop words on stream.

Words on stream can't be started until the word has been set with `c!set_word word`.

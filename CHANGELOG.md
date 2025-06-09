# Changelog

## [1.0.0] - TBD

## [1.0.0+pre1] - 2025-06-08

This is our first prerelease of version [1.0.0](#100---tbd). Also because of the way we committed code last time [0.1.3](#013snapshot25w24a---2025-06-08)'s code was a little corrupt.

### Changed

- Changed the name of the project to muddybot

### Added

- Added some error handling for when users don't send arguments with commands that require arguments

### Removed

- Removed !wordleonwheels command
- Removed unused except `KeyboardInterrupt:` code block
- Some unused classifiers in pyproject.toml

## [0.1.3+snapshot25w24a] - 2025-06-08

### Changed

- Changed wordsOnStream to wordleonwheels
- Moved Config file stuff to files.py
- Moved time code to make it more accurate
- Now using "%" formatting in logging functions: [logging-fstring-interpolation / W1203](https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/logging-fstring-interpolation.html)
- Put the bot's code in twitch_bot.py
- Changed c!online to c!status
- Moved logging functionality to logger.py
- Automatically stops searching for word when a user correctly guess the word.

### Added

- Added c!mud_curses command
- Added more comments and docstrings
- Added a way to get word into the program :)

### Removed

- Removed 'word' field in config.toml

## [0.1.2+snapshot25w23b] - 2025-06-07

### Added

- Added classifiers in pyproject.toml
- Added channel field to config file
- Added chat message logging

### Changed

- Changed some values in pyproject.toml
- Changed some formatting in CHANGELOG.md
- Deletes log file on startup
- Changed config file from config.json to config.toml
- Changed log file from log.txt to twbot.log

### Fixed

- Fixed some fields in pyproject.toml

## [0.1.1+snapshot25w23a] - 2025-06-06

### Added

- Added command line argument parsing
- Added a response to the boop command

### Changed

- Changed what is logged
- Now correctly is spelled the right way in \_\_main\_\_.py:64

### Fixed

- Fixed logging to console

## [0.1.0] - 2025-06-06

_Initial release_

[0.1.0]: https://github.com/TheCrunching/python-twitch-bot/releases/tag/v0.1.0
[0.1.1+snapshot25w23a]: https://github.com/TheCrunching/python-twitch-bot/releases/tag/v0.1.1+snapshot25w23a
[0.1.2+snapshot25w23b]: https://github.com/TheCrunching/python-twitch-bot/releases/tag/v0.1.2+snapshot25w23b
[0.1.3+snapshot25w24a]: https://github.com/TheCrunching/python-twitch-bot/releases/tag/v0.1.3+snapshot25w24a
[1.0.0+pre1]: https://github.com/TheCrunching/python-twitch-bot/releases/tag/v1.0.0+pre1
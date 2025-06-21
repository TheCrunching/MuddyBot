#!/usr/bin/env python3
"""Has file stuff for my code :)

**FILES**

* ~/.muddybot/ | Bot directory
* ~/.muddybot/muddy.log | Log file
* ~/.muddybot/config.toml | Config file
* ~/.muddybot/chat-{time}.log | Twitch chat log
"""

from pathlib import Path
from datetime import datetime, timezone

DATA_DIR = Path(Path.home(), ".muddybot/")
LOG_FILE = Path(DATA_DIR, "muddybot.log")
CONFIG_FILE = Path(DATA_DIR, "config.toml")

if not DATA_DIR.exists():  # Make sure log dir exists
    DATA_DIR.mkdir()  # If it does not exist create it


def get_chat_log_file():
    """Generates the log file for chat"""
    return Path(
        DATA_DIR,
        f"chat-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.log"
    )

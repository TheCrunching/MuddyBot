#!/usr/bin/env python3
"""Has file stuff for my code :)

**FILES**

* ~/.muddybot/ | Bot directory
* ~/.muddybot/muddy.log | Log file
* ~/.muddybot/config.toml | Config file
* ~/.muddybot/chat-{time}.log | Twitch chat log
"""

from pathlib import Path
from os import mkdir
from datetime import datetime

DATA_DIR = Path(Path.home(), ".muddybot/")
if not Path(DATA_DIR).exists():
    mkdir(DATA_DIR)

LOG_FILE = Path(DATA_DIR, "muddybot.log")
CHAT_LOG_FILE = Path(DATA_DIR, f"chat-{datetime.today().strftime('%Y-%m-%d')}.log")

CONFIG_FILE = Path(DATA_DIR, "config.toml")

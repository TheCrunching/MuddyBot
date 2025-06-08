#!/usr/bin/env python3
"""Has file stuff for my code :)

**FILES**

* ~/.twbot/ | Bot directory
* ~/.twbot/twbot.log | Log file
* ~/.twbot/config.toml | Config file
* ~/.twbot/chat-{time}.log | Twitch chat log
"""

from pathlib import Path
from os import mkdir
from datetime import datetime

DATA_DIR = Path(Path.home(), ".twbot/")
if not Path(DATA_DIR).exists():
    mkdir(Path(Path.home()))

LOG_FILE = Path(DATA_DIR, "twbot.log")
CHAT_LOG_FILE = Path(DATA_DIR, f"chat-{datetime.today().strftime('%Y-%m-%d')}.log")

CONFIG_FILE = Path(DATA_DIR, "config.toml")

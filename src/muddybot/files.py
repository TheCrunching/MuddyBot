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
if not DATA_DIR.exists():
    DATA_DIR.mkdir()

LOG_FILE = Path(DATA_DIR, "muddybot.log")
def getChatLogFile():
    return Path(DATA_DIR, f"chat-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.log")

CONFIG_FILE = Path(DATA_DIR, "config.toml")

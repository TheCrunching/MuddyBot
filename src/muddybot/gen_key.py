#!/usr/bin/env python3
"""Generates encryption key for muddybot"""

from cryptography.fernet import Fernet


def main():
    """Generates and prints the key"""

    print(f"Your key is: '{Fernet.generate_key().decode()}' keep this a secret. This needs to go in your configuration file under the key field.")  # Print key

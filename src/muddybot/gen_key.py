#!/usr/bin/env python3
"""Generates encryption key for muddybot"""
from cryptography.fernet import Fernet

def main():
    """Generates and prints the key

    Returns:
        int: Exit code
    """
    key = Fernet.generate_key().decode()# Generate key

    print(f"Your key is: '{key}' keep this a secret.")# Print key
    print("Puts this in your configuration file under the 'key' field.")

    return 0

if __name__ == "__main__":
    main()

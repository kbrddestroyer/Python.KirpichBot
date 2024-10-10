"""
Entrypoint, invoked from start.sh script or manually
Calls botcore.py initialize() method

Author:         kbrddestroyer
Last modify:    10.10.24 21:00
"""

import botcore


if __name__ == "__main__":
    botcore.initialize()

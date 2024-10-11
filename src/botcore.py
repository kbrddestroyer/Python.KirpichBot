"""
BotCore - main bot file, containing core logic and flow
Contains classes and entrypoint that's being called from main.py
"""

import os
import configparser
import discord

from typing import Optional
from discord import app_commands
from commands import BotCommandRegistry, BotCommand
from tools import tools, configuring


class BotCore:
    """
    Main bot class, contains core logic
    """

    BOT_CONFIG = "botconfig.ini"

    def __init__(self):
        self.__config: Optional[configparser.SectionProxy] = self.parse_config()
        if not self.__config:
            raise RuntimeError(f'Could not create bot: no {BotCore.BOT_CONFIG} provided')

        self.__token: str = self.__config.get("TOKEN")

        if not self.__token:
            raise RuntimeError('Could not create bot: no token provided')

        self.bot: discord.Client = discord.Client(intents=discord.Intents.all())
        self.tree: app_commands.CommandTree = app_commands.CommandTree(self.bot)
        self.registry: BotCommandRegistry = BotCommandRegistry(self.bot, self.tree)
        
        BotCommand.create(
            self.ping,
            'ping',
            'Shows bot online status and latency'
        )

    def parse_config(self) -> Optional[configparser.SectionProxy]:
        """
        Parses bot config with ConfigParser
        @returns SectionProxy
        """

        configpath = os.getenv('CONFIGPATH')
        if not configpath:
            configpath = "./"
        print(f'[DEBUG] Configpath is {configpath}')

        config = configparser.ConfigParser()
        config.read(configpath + BotCore.BOT_CONFIG)
        try:
            return config["BOT"]
        except KeyError:
            print('[ERROR] Could not parse initial config')
            return None

    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Pong! Latency: {self.bot.latency * 1000}ms')

    def run(self):
        """Interface function to run discord bot"""
        self.bot.run(self.__token)


def initialize():
    """
    Entrypoint, called from main.py

    @see main.py
    """

    bot = BotCore()
    tools.initialize()
    configuring.initialize()
    bot.run()


if __name__ == "__main__":
    print("[WARNING] Accessing bot core directly from botcore.py file!")
    initialize()

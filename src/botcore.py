"""
BotCore - main bot file, containing core logic and flow
Contains classes and entrypoint that's being called from main.py
"""

import configparser
import discord

from discord import app_commands
from commands import BotCommandRegistry, BotCommand
from tools import tools, configuring


class BotCore:
    """
    Main bot class, contains core logic
    """

    BOT_CONFIG = "botconfig.ini"

    def __init__(self):
        self.__config: configparser.SectionProxy = self.parse_config()
        self.__token: str = self.__config["TOKEN"]

        self.bot: discord.Client = discord.Client(intents=discord.Intents.all())
        self.tree: app_commands.CommandTree = app_commands.CommandTree(self.bot)
        self.registry: BotCommandRegistry = BotCommandRegistry(self.bot, self.tree)
        
        BotCommand.create(
            self.ping,
            'ping',
            'Shows bot online status and latency'
        )

    def parse_config(self) -> configparser.SectionProxy:
        """
        Parses bot config with ConfigParser
        @returns SectionProxy
        """

        config = configparser.ConfigParser()
        config.read(BotCore.BOT_CONFIG)
        return config["BOT"]

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

    print("[WARNING] Accessing bot core directly from botcore.py file!")

    bot = BotCore()
    tools.initialize()
    configuring.initialize()
    bot.run()


if __name__ == "__main__":
    initialize()

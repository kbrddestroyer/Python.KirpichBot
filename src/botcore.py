import configparser
import discord

from discord import app_commands
from commands import BotCommandRegistry
from tools import tools, configuring


class BotCore:
    """
    Main bot class, contains core logic
    """

    BOT_CONFIG = "botconfig.ini"

    def __init__(self):
        self.__config = self.__parse_config()
        self.__token = self.__config["TOKEN"]
        self.intents = discord.Intents.all()
        self.bot = discord.Client(intents=self.intents)
        self.tree = app_commands.CommandTree(self.bot)
        self.registry = BotCommandRegistry(self.bot, self.tree)

    def __parse_config(self) -> configparser.SectionProxy:
        config = configparser.ConfigParser()
        config.read(BotCore.BOT_CONFIG)
        return config["BOT"]

    def run(self):
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

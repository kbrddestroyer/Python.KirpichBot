import discord

from dataclasses import dataclass
from typing import List, Optional, Callable
from discord import app_commands


@dataclass
class BotCommand:
    func: Callable
    name: str
    description: Optional[str]

    @staticmethod
    def create(func: Callable, name: str, description: Optional[str]=None):
        global g_registry
        command = BotCommand(func, name, description)
        g_registry.register_command(command)


class BotCommandRegistry:
    def __init__(self, bot: discord.Client, tree: app_commands.CommandTree) -> None:
        global g_registry
        self.bot: discord.Client = bot
        self.tree: app_commands.CommandTree = tree
        self.__commands = []

        @self.bot.event
        async def on_ready():
            for command in self.__commands:
                print(f'[DEBUG] Registering {command.name}')
                self.__add_command(command)
            
            print('[DEBUG] Finish!')
            await self.tree.sync()

        g_registry = self

    def register_command(self, command: BotCommand):
        self.__commands.append(command)

    def __add_command(self, command: BotCommand):
        self.tree.add_command(
            app_commands.Command(
                callback=command.func,
                name=command.name,
                description=command.description if command.description else "",
            )
        )

    def register_range(self, commands: List[BotCommand]):
        for command in commands:
            self.register_command(command)


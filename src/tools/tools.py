import discord

from commands import BotCommand


class BotTools:
    def __init__(self) -> None:
        BotCommand.create(
            self.ping,
            'ping',
            'indev command'
        )        

    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')


def initialize():
    BotTools()


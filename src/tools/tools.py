import discord

from typing import Optional

from discord import app_commands
from commands import BotCommand
from tools.configuring import get_instance as config, ConfigKeys


class BotTools:
    def __init__(self) -> None:
        BotCommand.create(
            self.ping,
            'ping',
            'indev command'
        )        
        
        BotCommand.create(
            self.create_role, 
            'create_role',
            'Creates new role'
        )

        BotCommand.create(
            self.create_channel,
            'create_channel',
            'creates channel'
        )

    async def ping(self, interaction: discord.Interaction):
        config_instance = config()
        assert config_instance
        role = config_instance.as_role(ConfigKeys.ADMIN_ROLE, interaction)
        assert role
        print(role.name)
        if isinstance(interaction.user, discord.Member):
            if role not in interaction.user.roles:
                return
        await interaction.response.send_message('Pong!')

    @app_commands.describe(name='Name of the role')
    async def create_role(self, interaction: discord.Interaction, name: str):
        await interaction.guild.create_role(name=name)

    @app_commands.describe(section_name='Section name to create channel in')
    @app_commands.describe(channel_name='Name of the channel to create')
    @app_commands.describe(is_closed='Closed channel')
    @app_commands.describe(access_role='Role that has access to closed channel')
    async def create_channel(
            self,
            interaction: discord.Interaction, 
            section_name: str, 
            channel_name: str, 
            is_closed: bool=False,
            access_role: Optional[discord.Role]=None
        ):
        if not interaction.guild:
            await interaction.response.send_message('Trying to create channel while not in guild.')
            return
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message('Not a member')
            return
        if not config() or config().as_role(ConfigKeys.ADMIN_ROLE, interaction) not in interaction.user.roles:
            await interaction.response.send_message('Not an admin')
            return
        if access_role == interaction.guild.default_role:
            await interaction.response.send_message('Cannot create closed channel with everyone as access_role')
            return
        if access_role and isinstance(interaction.user, discord.Member) and access_role not in interaction.user.roles:
            await interaction.response.send_message('Cannot create closed channel: access_role not assigned to you')
            return

        overwrites = {}
        
        if is_closed or access_role:
            overwrites[interaction.guild.default_role] = discord.PermissionOverwrite(read_messages=False)
            overwrites[access_role if access_role else interaction.user] = discord.PermissionOverwrite(read_messages=True)

        category = await interaction.guild.create_category_channel(section_name, overwrites=overwrites)
        await interaction.guild.create_text_channel(channel_name, category=category)
        await interaction.response.send_message(f'Created {channel_name} in {section_name}')

def initialize():
    BotTools()


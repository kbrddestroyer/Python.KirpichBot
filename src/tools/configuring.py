import json
import discord

from typing import Dict, Any, Optional
from discord import app_commands
from commands import BotCommand


class ConfigKeys(discord.Enum):
    ADMIN_ROLE = ('admin_role', lambda val: len(val.split('<@&')) > 1)
    CAN_CREATE_CHANNELS = ('Can create channels', lambda val: val in ('True', 'False'))


class BotConfiguring:
    CONFIG_PATH = './config/botconfig.json'

    def __init__(self) -> None:
        self.__data: Dict = self.__load_config()

        BotCommand.create(
            self.change_config_item,
            'change_config',
            'Change config param for current guild'
        )

    def __save_config(self):
        """
        Saves stored configuration to file
        """
        print('[DEBUG] Writing config data')
        with open(BotConfiguring.CONFIG_PATH, 'w') as f:
            data = json.dumps(self.__data, indent=4)
            f.write(data)

    def __load_config(self) -> Dict:
        data = {}
        try:
            with open(BotConfiguring.CONFIG_PATH, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print('[ERROR] FileNotFoundError: couldn\'t open config file')
            return {}
        print(f'[DEBUG] Opened {BotConfiguring.CONFIG_PATH} and read the contents {data}')
        return data

    def __getitem__(self, key: ConfigKeys) -> Any:
        return self.__data.get(key.value[0])

    def as_role(self, key: ConfigKeys, interaction: discord.Interaction) -> Optional[discord.Role]:
        guild_config = self.__data.get(interaction.guild_id, {})
        value = guild_config.get(key.value[0])
        if not value:
            return None
        role_id = None
        try:
            role_id = value.split('<@&')[1][:-1]
        except IndexError:
            return None
        assert interaction.guild
        return interaction.guild.get_role(int(role_id))

    @app_commands.describe(key='Config key')
    @app_commands.describe(value='Config value')
    async def change_config_item(self, interaction: discord.Interaction, key: ConfigKeys, value: str):
        if not interaction.guild:
            await interaction.response.send_message('Cannot config DMs')
            return
        print(f'[DEBUG] Changed config value in {interaction.guild.name} {key.value}: {value}')
        guild_config = self.__data.setdefault(interaction.guild_id, {})
        
        config_key, validator = key.value
        if not validator(value):
            await interaction.response.send_message('Wrong value passed')
            return

        guild_config[config_key] = value
        self.__save_config()
        await interaction.response.send_message('Changed config value')

def initialize():
    global g_instance
    g_instance = BotConfiguring()


def get_instance() -> Optional[BotConfiguring]:
    global g_instance
    return g_instance

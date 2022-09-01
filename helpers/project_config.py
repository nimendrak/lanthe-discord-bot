from collections import namedtuple
from helpers.json_manager import json_load as JsonLoader
from helpers.singleton import Singleton

class ProjectConfigManager(metaclass=Singleton):    
    def __init__(self, json_path: str) -> None:
        
        # Load config fille to the project manager
        self.proj_config = JsonLoader(json_path)
        
    def get_bots_config(self) -> namedtuple:
        """
        Load bot config data from json file
        """
        # Initialize bot configs
        Bot = namedtuple("Bot", ["bot", "config"])
        return Bot(bot="notifications_bot", config=self.proj_config['NOTIFICATIONS_BOT'])

    def get_guild_data(self) -> dict:
        """
        Get guild data from json file
        """
        return self.proj_config['GUILD_DATA']

from cogs.embeds.general import cogs_info
from helpers.project_config import ProjectConfigManager
from helpers.logger_config import logger as log

from helpers.singleton import Singleton
import logging
import nextcord
from nextcord.ext import commands
from pathlib import Path

# Create a instance of pcm to get all the project config data
pcm = ProjectConfigManager()

log = logging.getLogger(__name__)

class BotConfigManager(metaclass=Singleton):
    def __init__(self, client: nextcord.ext.commands.Bot) -> None:
        self.client = client

    def initialize(self):
        # Load all cogs
        cogs = [path.stem for path in Path("cogs").glob("*.py")]
        for cog in cogs:
            try:
                self.client.load_extension(f"cogs.{cog}")
                log.info(f"Loaded cog | {cog}")
            except commands.NoEntryPointError:
                log.warning(f"No Entry Pointer | {cog}")
                pass

    # Load bot cogs from directory
    async def load_cogs(self, ctx: commands.Context, subdir: str):
        cog = [Path(f"{subdir}").stem][0]
        try:
            try:
                self.client.load_extension(f"cogs.{cog}")
                
                await cogs_info(ctx, f"**{cog}** has been loaded to Goofy Guard")
                log.info(f"Loaded a single cog | {cog}")
            except commands.ExtensionNotFound:
                await cogs_info(ctx, f"This extension does not exist.")
                log.warning(f"Could not found the cog | {cog}")
        except commands.ExtensionAlreadyLoaded:
            await cogs_info(ctx, f"This extension is already loaded.")
            log.warning(f"{cog} | is already loaded")

    # Unload bot cogs from directory
    async def unload_cogs(self, ctx:commands.Context, subdir: str):
        cog = [Path(f"{subdir}").stem][0]
        try:
            try:
                self.client.unload_extension(f"cogs.{cog}")
                
                await cogs_info(ctx, f"**{cog}** has been unloaded from Goofy Guard")
                log.info(f"Unloaded a single cog | {cog}")
            except commands.ExtensionNotLoaded:
                await cogs_info(ctx, f"This extension has be to loaded first.")
                log.warning(f"{cog} | has be to loaded first")               
        except commands.ExtensionNotFound:
            await cogs_info(ctx, f"This extension does not exist.")
            log.warning(f"Cogs does not exsit | {cog}")
                
    # Unload cogs then load again to reload cogs            
    async def reload_cogs(self, ctx:commands.Context, cog_name: str):
        cog = [Path(f"{cog_name}").stem][0]
        try:
            try:
                self.client.unload_extension(f"cogs.{cog}")
                self.client.load_extension(f"cogs.{cog}")
                
                await cogs_info(ctx, f"**{cog}** has been reloaded to Goofy Guard")
                log.info(f"Reloaded a single cog | {cog}")
            except commands.ExtensionAlreadyLoaded:
                await cogs_info(ctx, f"This extension is already loaded.")
                log.warning(f"{cog} | is already loaded")              
        except commands.ExtensionNotFound:
            await cogs_info(ctx, f"This extension does not exist.")
            log.warning(f"Cogs does not exsit | {cog}")   
            
    # Set avatar to each bot        
    async def set_avatar(self, avatar_url: str):
        await self.client.wait_until_ready()
        try:
            with open(avatar_url, "rb") as pfp:
                await self.client.user.edit(avatar=pfp.read())
                log.info(f"Set avatar to {self.client.user}")
        except:
            log.error(f"Failed to set avatar to {self.client.user}")
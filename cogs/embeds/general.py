from helpers.logger_config import logger as log
from helpers.project_config import ProjectConfigManager
import logging
import nextcord
from nextcord.ext import commands

# Get project config instance
pcm = ProjectConfigManager("config.json")

# Initialize and load guild, guard data
GUILD_DATA = pcm.get_guild_data()

log = logging.getLogger(__name__)

async def cogs_info(context: commands.Context, content:str):
    embed = nextcord.Embed(
        title="Cogs Manager",
        description=content,
        color=nextcord.Color(int(GUILD_DATA.get("EMBED_COLOR"), 16))
    )
    await context.reply(embed=embed)
    log.info(f"Cogs info embed has been sent to {context.channel}")

async def db_info(context: commands.Context, content:str):
    embed = nextcord.Embed(
        title="Database Manager",
        description=content,
        color=nextcord.Color(int(GUILD_DATA.get("EMBED_COLOR"), 16))
    )
    await context.reply(embed=embed)
    log.info(f"db info embed has been sent to {context.channel}")
    
from cogs.embeds.general import cogs_info
from helpers.bot_config import BotConfigManager
from helpers.project_config import ProjectConfigManager
from helpers.logger_config import logger as log
from flask import Flask 
from threading import Thread
import logging
import nextcord
from nextcord.ext.commands import Bot
from nextcord.ext import commands
from pathlib import Path

app = Flask('nextcord bot')

@app.route('/')
def home():
    return 'Hi, Notifications Centre is alive!'

def start_server():
  app.run(host='0.0.0.0',port=8080)
  
t = Thread(target=start_server)
t.start()

log = logging.getLogger(__name__)

# Create a instance of pcm to get all the project config data
pcm = ProjectConfigManager("config.json")
log.info(f"pcm @ {pcm}")

# Initialize bot, db configs and load guild data
BOT = pcm.get_bots_config()
GUILD_DATA = pcm.get_guild_data()

notifications_centre = Bot(
    command_prefix=BOT.config["bot_prefix"],
    intents=nextcord.Intents.all(),
    status=nextcord.Status.online,
    activity=nextcord.Game(name="Head of Notifications")
)
notifications_centre.remove_command("help")

# Initialize bcm to load, unload cogs and set avatar
bcm = BotConfigManager(notifications_centre)
bcm.initialize()
log.info(f"bcm @ {bcm}")

@commands.has_permissions(administrator=True)
@notifications_centre.command(name="cogs", aliases=["cg"])
async def get_cogs(ctx: commands.Context):
    cogs = [path.stem for path in Path(f"cogs").glob("*.py")]
    await cogs_info(ctx, "Notifications Centre cogs as follows:```{}```".format("\n".join(cogs)))

@commands.has_permissions(administrator=True)
@notifications_centre.command(name="load", aliases=["l", "ld"])
async def load_cog(ctx: commands.Context, cog_name: str):
    await bcm.load_cogs(ctx, f"cogs/{cog_name}.py")

@commands.has_permissions(administrator=True)
@notifications_centre.command(name="unload", aliases=["ul", "uld"])
async def unload_cog(ctx: commands.Context, cog_name:str): 
    await bcm.unload_cogs(ctx, f"cogs/{cog_name}.py")

@commands.has_permissions(administrator=True)
@notifications_centre.command(name="reload", aliases=["rl", "rld"])
async def reload_cog(ctx: commands.Context, cog_name: str):    
    await bcm.reload_cogs(ctx, f"cogs/{cog_name}.py")

@commands.has_permissions(administrator=True)
@notifications_centre.command(name="cogs_help", aliases=["cogs_hp", "cgs_hp"])
async def admin_help(self, context: commands.Context):
    embed=nextcord.Embed(
        title="**Notifications Centre Cogs Manager**",
        description=f"""
        **You can interact with the Cogs Manager by using the following commands:**
        > `{BOT.config["bot_prefix"]}cogs` [aliases: cg] - Get names of loaded cogs.
        > `{BOT.config["bot_prefix"]}load <cog_name>` [aliases: l, ld] - Load a single cog. 
        > `{BOT.config["bot_prefix"]}unload <cog_name>` [aliases: ul, uld] - Unload a single cog.
        > `{BOT.config["bot_prefix"]}reload <cog_name>` [aliases: rl, rld] - Unload and load again, a single cog.
        \n**Cogs Manager Interactions only available for following roles:**
        > **<@&{GUILD_DATA.get("AUTH_ROLES_ID")[0]}>**
        """,
        color=nextcord.Color(int(GUILD_DATA.get("EMBED_COLOR"), 16))
    )
    await context.reply(embed=embed)
    log.info(f"{context.author} used the admin help command")

notifications_centre.run(BOT.config["token"], reconnect=True)
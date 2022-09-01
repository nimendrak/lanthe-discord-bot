from helpers.logger_config import logger as log
from helpers.project_config import ProjectConfigManager
import logging
import nextcord
from nextcord.ext import commands

# Get project config instance
pcm = ProjectConfigManager()

# Initialize and load guild, guard data
GUILD_DATA = pcm.get_guild_data()

log = logging.getLogger(__name__)
        
class GuardExceptions(commands.Cog, name="Guard Exceptions"):
    def __init__(self, client):
        self.client = client
            
    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                title="Notifications Centre",
                description=f"You do not have permission to use this command.",
                color=nextcord.Color(int(GUILD_DATA.get("EMBED_COLOR"), 16))
            )
            log.warning(f"{context.author} tried to use {context.command.name} but has no permission.")
            return await context.reply(embed=embed, mention_author=False)

        if isinstance(error, commands.CommandNotFound):
            embed = nextcord.Embed(
                title="Notifications Centre",
                description=f"This command does not exist.",
                color=nextcord.Color(int(GUILD_DATA.get("EMBED_COLOR"), 16))
            )
            log.warning(f"{context.author} tried to use {context.message.content} but the command does not exist.")
            return await context.reply(embed=embed, mention_author=False)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(
                title="Notifications Centre",
                description=f"You are missing a required argument.",
                color=nextcord.Color(int(GUILD_DATA.get("EMBED_COLOR"), 16))
            )
            log.warning(f"{context.author} tried to use {context.message.content} but is missing a required argument.")
            return await context.reply(embed=embed, mention_author=False)

        if isinstance(error, commands.BadArgument):
            embed = nextcord.Embed(
                title="Notifications Centre",
                description=f"You have provided an invalid argument.",
                color=nextcord.Color(int(GUILD_DATA.get("EMBED_COLOR"), 16))
            )
            log.warning(f"{context.author} tried to use {context.message.content} but is providing an invalid argument")
            return await context.reply(embed=embed, mention_author=False)

        if isinstance(error, commands.MissingRole):
            embed = nextcord.Embed(
                title="Notifications Centre",
                description=f"You are missing a required role to execute this command.",
                color=nextcord.Color(int(GUILD_DATA.get("EMBED_COLOR"), 16))
            )
            log.warning(f"{context.author} tried to use {context.message.content} but is missing a required role.")
            return await context.reply(embed=embed, mention_author=False)
        
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            
            embed = nextcord.Embed(
                title="Notifications Centre",
                description=f"You are on cooldown. You can use this command again in **{f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.**",
                color=nextcord.Color(int(GUILD_DATA.get("EMBED_COLOR"), 16))
            )
            log.warning(f"{context.author} tried to use {context.message.content} but is on cooldown.")
            return await context.reply(embed=embed, mention_author=False)
        
def setup(client):
    client.add_cog(GuardExceptions(client)) 

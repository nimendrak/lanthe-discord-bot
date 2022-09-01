from random import choices
from helpers.logger_config import logger as log
from helpers.project_config import ProjectConfigManager
from helpers.bot_config import BotConfigManager
import logging
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import time

# Get project config instance
pcm = ProjectConfigManager()

BOT = pcm.get_bots_config()
GUILD_DATA = pcm.get_guild_data()

log = logging.getLogger(__name__)
        
class Notifications(commands.Cog, name="Notifications Cog"):
    def __init__(self, client):
        self.client = client
        self.bcm = BotConfigManager()

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f"Logged in as {str(self.client.user)}")
        log.info(f"Logged in time: {time.strftime('%a, %d %b %Y %H:%M:%S')}")
        await self.bcm.set_avatar(BOT.config["bot_avatar"])

    @nextcord.slash_command(name="notify", description="Notify people about the content updates (Admin Only)", guild_ids=[GUILD_DATA.get("GUILD_ID")])
    async def notify(
        self,
        interaction: Interaction,
        link: str,
        platform: str = SlashOption(
            name="picker",
            choices={"Tiktok": "tt", "Youtube Short": "yts", "Youtube Video": "ytv", "TikTok Live": "ttl"},
        ),
    ):
        mention_everyone = nextcord.AllowedMentions(everyone = True)
        announcement_channel = self.client.get_channel(GUILD_DATA.get("ANNOUNCEMENTS_CHANNEL"))
        content_updates_channel = self.client.get_channel(GUILD_DATA.get("CONTENT_UPDATES_CHANNEL"))

        if GUILD_DATA.get("AUTH_ROLES_ID")[0] in [role.id for role in interaction.user.roles]:
            if platform == "tt":
                await content_updates_channel.send(
                    content = f"""
                    @ everyone
                    > BOT Lanthe posted a new clip on TikTok. Make sure you check it out!. **Link:** {link}
                    """,
                    allow_mentions = mention_everyone
                )
            elif platform == "yts":
                await content_updates_channel.send(
                    content = f"""
                    @ everyone
                    > Bot Lanthe just uploaded a Youtube Short. Make sure you check it out!. **Link:** {link}
                    """,
                    allow_mentions = mention_everyone
                )
            elif platform == "ytv":
                await content_updates_channel.send(
                    content = f"""
                    @ everyone
                    > Bot Lanthe uploaded a full Youtube video. Make sure you check it out!. **Link:** {link}
                    """,
                    allow_mentions = mention_everyone
                )
            elif platform == "ttl":
                await announcement_channel.send(
                    content = f"""
                    @ everyone
                    > We're streaming live on TikTok, follow this link to check it out. **Link:** {link}
                    """,
                    allow_mentions = mention_everyone
                )
            await interaction.response.send_message(f"Notification has been sent.", ephemeral=False)
            log.warning(f"{interaction.user} sent a notification to | {content_updates_channel}") 
        else:
            await interaction.response.send_message(f"You don't have the required permissions to use this command.", ephemeral=False)
            log.warning(f"User tried to use a notification command | { interaction.user.roles}") 

def setup(client):
    client.add_cog(Notifications(client))

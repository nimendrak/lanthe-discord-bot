from helpers.logger_config import logger as log
from helpers.project_config import ProjectConfigManager
from helpers.bot_config import BotConfigManager
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import time
from datetime import datetime
from dateutil.tz import gettz

# Get project config instance
pcm = ProjectConfigManager()

BOT = pcm.get_bots_config()
GUILD_DATA = pcm.get_guild_data()
        
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
        link: str = SlashOption(
            description="Link to the published content",
        ),
        platform: str = SlashOption(
            name="picker",
            description="Select the type your content",
            choices={"TikTok Post": "tt", "Youtube Short": "yts", "Youtube Video": "ytv", "TikTok Live": "ttl"},
        ),
    ):
        live_updates_channel = self.client.get_channel(GUILD_DATA.get("LIVE_UPDATES_CHANNEL"))
        yt_updates_channel = self.client.get_channel(GUILD_DATA.get("YT_UPDATES_CHANNEL"))      
        tt_updates_channel = self.client.get_channel(GUILD_DATA.get("TT_UPDATES_CHANNEL"))

        current_time = datetime.now(gettz("Asia/Colombo")).strftime("%a, %d %b %Y %H:%M:%S")

        if GUILD_DATA.get("AUTH_ROLES_ID")[0] in [role.id for role in interaction.user.roles]:
            if platform == "tt":
                await tt_updates_channel.send(
                    content = f"""
                    @everyone
                    > BOT Lanthe posted a new clip on TikTok. Make sure you check it out!. **Link:** {link}
                    """,
                )
                await interaction.response.send_message(f"{interaction.user.mention} sent a **TikTok Post** notification @ {current_time}", ephemeral=False)
            elif platform == "yts":
                await yt_updates_channel.send(
                    content = f"""
                    @everyone
                    > Bot Lanthe just uploaded a Youtube Short. Make sure you check it out!. **Link:** {link}
                    """,
                )
                await interaction.response.send_message(f"{interaction.user.mention} sent a **Youtube Short** notification @ {current_time}", ephemeral=False)
            elif platform == "ytv":
                await yt_updates_channel.send(
                    content = f"""
                    @everyone
                    > Bot Lanthe uploaded a full Youtube video. Make sure you check it out!. **Link:** {link}
                    """,
                )
                await interaction.response.send_message(f"{interaction.user.mention} sent a **Youtube Video** notification @ {current_time}", ephemeral=False)
            elif platform == "ttl":
                await live_updates_channel.send(
                    content = f"""
                    @everyone
                    > We're streaming live on TikTok, follow this link to check it out. **Link:** {link}
                    """,
                )
                await interaction.response.send_message(f"{interaction.user.mention} sent a **TikTok Live** notification @ {current_time}", ephemeral=False)
            log.warning(f"{interaction.user} sent a notification") 
        else:
            await interaction.response.send_message("You don't have the required permissions to use this command.", ephemeral=False)
            log.warning(f"User tried to use a notification command | { interaction.user.mention}") 

def setup(client):
    client.add_cog(Notifications(client))

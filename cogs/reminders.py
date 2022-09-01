from helpers.logger_config import logger as log
from helpers.project_config import ProjectConfigManager
import logging
import time
from datetime import datetime
from dateutil.tz import gettz
from nextcord.ext import commands, tasks
import time

# Get project config instance
pcm = ProjectConfigManager()

GUILD_DATA = pcm.get_guild_data()

log = logging.getLogger(__name__)
        
class Reminders(commands.Cog, name="Reminders Cog"):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.private_lobby_reminder.start()

    @tasks.loop(seconds=1)
    async def private_lobby_reminder(self):
        current_time = datetime.now(gettz("Asia/Colombo")).strftime("%H:%M:%S")
        lanthe_only_channel = self.client.get_channel(GUILD_DATA.get("LANTHE_ONLY_CHANNEL"))
    
        if(current_time == '21:30:00'):
            await lanthe_only_channel.send(
            content = f"""
                <@&{GUILD_DATA.get("LANTHE_CLAN_ROLE")}>
                > **It's time to play private lobbies!**
                > {time.strftime('%a, %d %b %Y')}
                """
            )
            log.info(f"private lobby reminder sent to <#{lanthe_only_channel}> channel")

def setup(client):
    client.add_cog(Reminders(client))

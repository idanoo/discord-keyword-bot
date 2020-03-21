import discord
import os
import re
from dotenv import load_dotenv

# https://discordpy.readthedocs.io/en/latest/api.html

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.channel.id == os.getenv("SOURCE_CHANNEL"):
            if re.match(os.getenv("REGEX_MATCH"), message.content, re.IGNORECASE):
                for channel_id in explode(os.getenv("DISCORD_CHANNELS")):
                    channel = client.get_channel(channel_id)
                    await channel.send('*' + message.content + '*')

load_dotenv()
client = MyClient()
client.run(os.getenv("DISCORD_TOKEN"), bot=False)
